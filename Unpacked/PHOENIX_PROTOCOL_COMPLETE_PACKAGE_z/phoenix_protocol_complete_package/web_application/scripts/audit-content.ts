/**
 * Content Audit Script
 * Scans all content files and generates a comprehensive audit report
 */

import { readFileSync, writeFileSync, readdirSync, statSync } from 'fs';
import { join, relative } from 'path';

interface ContentFile {
  path: string;
  type: string;
  size: number;
  lines: number;
  lastModified: Date;
  hasCodeBlocks: boolean;
  hasLinks: boolean;
  wordCount: number;
}

interface AuditReport {
  totalFiles: number;
  totalSize: number;
  totalLines: number;
  totalWords: number;
  filesByType: Record<string, number>;
  files: ContentFile[];
  timestamp: string;
}

function scanDirectory(dir: string, baseDir: string, results: ContentFile[] = []): ContentFile[] {
  const files = readdirSync(dir);
  
  for (const file of files) {
    const filePath = join(dir, file);
    const stat = statSync(filePath);
    
    // Skip node_modules, dist, and hidden directories
    if (file === 'node_modules' || file === 'dist' || file.startsWith('.')) {
      continue;
    }
    
    if (stat.isDirectory()) {
      scanDirectory(filePath, baseDir, results);
    } else if (file.endsWith('.md') || file.endsWith('.ts') || file.endsWith('.tsx')) {
      const content = readFileSync(filePath, 'utf-8');
      const lines = content.split('\n').length;
      const words = content.split(/\s+/).filter(w => w.length > 0).length;
      const hasCodeBlocks = /```/.test(content);
      const hasLinks = /\[.*\]\(.*\)/.test(content) || /https?:\/\//.test(content);
      
      results.push({
        path: relative(baseDir, filePath),
        type: file.endsWith('.md') ? 'markdown' : 'typescript',
        size: stat.size,
        lines,
        lastModified: stat.mtime,
        hasCodeBlocks,
        hasLinks,
        wordCount: words
      });
    }
  }
  
  return results;
}

function generateAuditReport(): AuditReport {
  const baseDir = process.cwd();
  const files = scanDirectory(baseDir, baseDir);
  
  const filesByType: Record<string, number> = {};
  let totalSize = 0;
  let totalLines = 0;
  let totalWords = 0;
  
  for (const file of files) {
    filesByType[file.type] = (filesByType[file.type] || 0) + 1;
    totalSize += file.size;
    totalLines += file.lines;
    totalWords += file.wordCount;
  }
  
  return {
    totalFiles: files.length,
    totalSize,
    totalLines,
    totalWords,
    filesByType,
    files: files.sort((a, b) => b.size - a.size),
    timestamp: new Date().toISOString()
  };
}

// Run audit
const report = generateAuditReport();

// Write report to JSON
writeFileSync(
  'content-audit-report.json',
  JSON.stringify(report, null, 2)
);

// Generate markdown summary
const markdown = `# Content Audit Report

Generated: ${report.timestamp}

## Summary Statistics

- **Total Files**: ${report.totalFiles}
- **Total Size**: ${(report.totalSize / 1024).toFixed(2)} KB
- **Total Lines**: ${report.totalLines.toLocaleString()}
- **Total Words**: ${report.totalWords.toLocaleString()}

## Files by Type

${Object.entries(report.filesByType)
  .map(([type, count]) => `- **${type}**: ${count} files`)
  .join('\n')}

## Top 20 Largest Files

| File | Type | Size (KB) | Lines | Words |
|------|------|-----------|-------|-------|
${report.files.slice(0, 20)
  .map(f => `| ${f.path} | ${f.type} | ${(f.size / 1024).toFixed(2)} | ${f.lines} | ${f.wordCount} |`)
  .join('\n')}

## Content Files with Code Examples

${report.files
  .filter(f => f.hasCodeBlocks)
  .map(f => `- ${f.path}`)
  .join('\n')}

## Content Files with External Links

${report.files
  .filter(f => f.hasLinks)
  .map(f => `- ${f.path}`)
  .join('\n')}
`;

writeFileSync('content-audit-report.md', markdown);

console.log('✅ Content audit complete!');
console.log(`📊 Scanned ${report.totalFiles} files`);
console.log(`📝 Total: ${report.totalLines.toLocaleString()} lines, ${report.totalWords.toLocaleString()} words`);
console.log(`💾 Reports saved: content-audit-report.json, content-audit-report.md`);
