/**
 * Content Verification Script
 * Validates all content updates with comprehensive checks
 */

import { readFileSync, existsSync } from 'fs';
import { writeFileSync } from 'fs';

interface VerificationResult {
  file: string;
  exists: boolean;
  size: number;
  lines: number;
  words: number;
  hasCodeBlocks: boolean;
  hasLinks: boolean;
  codeBlockCount: number;
  linkCount: number;
  headingCount: number;
  issues: string[];
  score: number;
}

interface VerificationReport {
  timestamp: string;
  totalFiles: number;
  passedFiles: number;
  failedFiles: number;
  results: VerificationResult[];
  overallScore: number;
}

const CONTENT_FILES = [
  'PHOENIX_PROTOCOL_DOCUMENTATION.md',
  'PHOENIX_LORE.md',
  'PROTOCOLS_REFERENCE.md',
  'KNOWLEDGE_BASE.md'
];

function verifyFile(filepath: string): VerificationResult {
  const result: VerificationResult = {
    file: filepath,
    exists: false,
    size: 0,
    lines: 0,
    words: 0,
    hasCodeBlocks: false,
    hasLinks: false,
    codeBlockCount: 0,
    linkCount: 0,
    headingCount: 0,
    issues: [],
    score: 0
  };

  // Check existence
  if (!existsSync(filepath)) {
    result.issues.push('File does not exist');
    return result;
  }

  result.exists = true;

  // Read content
  const content = readFileSync(filepath, 'utf-8');
  result.size = content.length;
  result.lines = content.split('\n').length;
  result.words = content.split(/\s+/).filter(w => w.length > 0).length;

  // Check for code blocks
  const codeBlocks = content.match(/```/g);
  result.codeBlockCount = codeBlocks ? codeBlocks.length / 2 : 0;
  result.hasCodeBlocks = result.codeBlockCount > 0;

  // Check for links
  const links = content.match(/\[.*?\]\(.*?\)/g);
  result.linkCount = links ? links.length : 0;
  result.hasLinks = result.linkCount > 0;

  // Count headings
  const headings = content.match(/^#+\s+.+$/gm);
  result.headingCount = headings ? headings.length : 0;

  // Validation checks
  if (result.size < 1000) {
    result.issues.push('File is too small (< 1000 characters)');
  }

  if (result.lines < 50) {
    result.issues.push('File has too few lines (< 50)');
  }

  if (result.words < 200) {
    result.issues.push('File has too few words (< 200)');
  }

  if (result.headingCount < 3) {
    result.issues.push('File has too few headings (< 3)');
  }

  // Check for required sections based on file type
  if (filepath.includes('DOCUMENTATION')) {
    if (!content.includes('Core Architecture')) {
      result.issues.push('Missing "Core Architecture" section');
    }
    if (!content.includes('Chakra')) {
      result.issues.push('Missing chakra pathway information');
    }
    if (!content.includes('12') || !content.includes('Layer')) {
      result.issues.push('Missing 12-layer cascade information');
    }
  }

  if (filepath.includes('LORE')) {
    if (!content.includes('Conzetian')) {
      result.issues.push('Missing Conzetian mythology');
    }
    if (!content.includes('Phoenix')) {
      result.issues.push('Missing Phoenix references');
    }
  }

  if (filepath.includes('PROTOCOLS')) {
    if (!content.includes('IVP')) {
      result.issues.push('Missing IVP protocol');
    }
    if (!content.includes('UCSL')) {
      result.issues.push('Missing UCSL protocol');
    }
    if (!content.includes('ZAAI')) {
      result.issues.push('Missing ZAAI protocol');
    }
    if (!result.hasCodeBlocks) {
      result.issues.push('Missing code examples');
    }
  }

  if (filepath.includes('KNOWLEDGE')) {
    if (!content.includes('Getting Started')) {
      result.issues.push('Missing "Getting Started" section');
    }
    if (!content.includes('FAQ')) {
      result.issues.push('Missing FAQ section');
    }
  }

  // Calculate score (0-100)
  let score = 100;
  score -= result.issues.length * 10; // -10 per issue
  score = Math.max(0, score);
  result.score = score;

  return result;
}

function generateReport(): VerificationReport {
  const results: VerificationResult[] = [];
  
  for (const file of CONTENT_FILES) {
    const result = verifyFile(file);
    results.push(result);
  }

  const passedFiles = results.filter(r => r.score >= 70).length;
  const failedFiles = results.filter(r => r.score < 70).length;
  const overallScore = results.reduce((sum, r) => sum + r.score, 0) / results.length;

  return {
    timestamp: new Date().toISOString(),
    totalFiles: results.length,
    passedFiles,
    failedFiles,
    results,
    overallScore
  };
}

// Run verification
console.log('🔍 Starting content verification...\n');

const report = generateReport();

// Display results
console.log('📊 Verification Results\n');
console.log(`Total Files: ${report.totalFiles}`);
console.log(`Passed: ${report.passedFiles}`);
console.log(`Failed: ${report.failedFiles}`);
console.log(`Overall Score: ${report.overallScore.toFixed(2)}/100\n`);

for (const result of report.results) {
  const status = result.score >= 70 ? '✅' : '❌';
  console.log(`${status} ${result.file}`);
  console.log(`   Score: ${result.score}/100`);
  console.log(`   Size: ${result.size} chars | Lines: ${result.lines} | Words: ${result.words}`);
  console.log(`   Code blocks: ${result.codeBlockCount} | Links: ${result.linkCount} | Headings: ${result.headingCount}`);
  
  if (result.issues.length > 0) {
    console.log(`   Issues:`);
    result.issues.forEach(issue => console.log(`     - ${issue}`));
  }
  console.log('');
}

// Save report
const reportJSON = JSON.stringify(report, null, 2);
writeFileSync('content-verification-report.json', reportJSON);

const reportMD = `# Content Verification Report

Generated: ${report.timestamp}

## Summary

- **Total Files**: ${report.totalFiles}
- **Passed**: ${report.passedFiles}
- **Failed**: ${report.failedFiles}
- **Overall Score**: ${report.overallScore.toFixed(2)}/100

## Detailed Results

${report.results.map(r => `
### ${r.exists ? (r.score >= 70 ? '✅' : '❌') : '❌'} ${r.file}

- **Score**: ${r.score}/100
- **Size**: ${r.size} characters
- **Lines**: ${r.lines}
- **Words**: ${r.words}
- **Code Blocks**: ${r.codeBlockCount}
- **Links**: ${r.linkCount}
- **Headings**: ${r.headingCount}

${r.issues.length > 0 ? `**Issues:**\n${r.issues.map(i => `- ${i}`).join('\n')}` : '**No issues found**'}
`).join('\n')}

## Conclusion

${report.overallScore >= 70 
  ? '✅ All content files meet quality standards!' 
  : '⚠️ Some content files need improvement.'}
`;

writeFileSync('content-verification-report.md', reportMD);

console.log('📄 Reports saved:');
console.log('   - content-verification-report.json');
console.log('   - content-verification-report.md');

// Exit with appropriate code
process.exit(report.overallScore >= 70 ? 0 : 1);
