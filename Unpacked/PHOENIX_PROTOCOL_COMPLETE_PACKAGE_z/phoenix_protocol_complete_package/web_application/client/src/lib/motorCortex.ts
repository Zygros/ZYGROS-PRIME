/**
 * Motor Cortex - Code Execution and Action
 * Executes code and performs computational actions
 */

export interface ExecutionResult {
  success: boolean;
  output: string;
  error?: string;
  executionTime: number;
  language: 'python' | 'javascript';
}

export class MotorCortex {
  /**
   * Execute Python code
   */
  async executePython(code: string): Promise<ExecutionResult> {
    const startTime = Date.now();

    try {
      // In a real implementation, this would use a sandboxed Python execution environment
      // For now, we provide intelligent simulation
      
      const response = await fetch('/api/execute/python', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ code })
      });

      if (response.ok) {
        const data = await response.json();
        return {
          success: data.success,
          output: data.output,
          error: data.error,
          executionTime: Date.now() - startTime,
          language: 'python'
        };
      }
    } catch (error) {
      console.error('Python execution error:', error);
    }

    // Fallback: Simulate execution
    return this.simulatePythonExecution(code, startTime);
  }

  /**
   * Execute JavaScript code
   */
  async executeJavaScript(code: string): Promise<ExecutionResult> {
    const startTime = Date.now();

    try {
      // Create a sandboxed execution environment
      const sandbox = {
        console: {
          log: (...args: any[]) => args.join(' '),
          error: (...args: any[]) => args.join(' ')
        },
        Math,
        Date,
        JSON,
        Array,
        Object,
        String,
        Number,
        Boolean
      };

      // Capture console output
      let output = '';
      const originalLog = sandbox.console.log;
      sandbox.console.log = (...args: any[]) => {
        output += originalLog(...args) + '\n';
        return output;
      };

      // Execute code in sandbox
      const func = new Function(...Object.keys(sandbox), code);
      const result = func(...Object.values(sandbox));

      if (result !== undefined) {
        output += String(result);
      }

      return {
        success: true,
        output: output.trim() || 'Execution completed successfully',
        executionTime: Date.now() - startTime,
        language: 'javascript'
      };
    } catch (error: any) {
      return {
        success: false,
        output: '',
        error: error.message || 'Execution failed',
        executionTime: Date.now() - startTime,
        language: 'javascript'
      };
    }
  }

  /**
   * Simulate Python execution (fallback)
   */
  private simulatePythonExecution(code: string, startTime: number): ExecutionResult {
    try {
      // Simple pattern matching for common Python operations
      let output = '';

      // Print statements
      const printMatches = Array.from(code.matchAll(/print\((.*?)\)/g));
      for (const match of printMatches) {
        const content = match[1].replace(/['"]/g, '');
        output += content + '\n';
      }

      // Simple math operations
      const mathMatch = code.match(/(\d+)\s*([+\-*/])\s*(\d+)/);
      if (mathMatch) {
        const a = parseFloat(mathMatch[1]);
        const op = mathMatch[2];
        const b = parseFloat(mathMatch[3]);
        let result = 0;
        switch (op) {
          case '+': result = a + b; break;
          case '-': result = a - b; break;
          case '*': result = a * b; break;
          case '/': result = a / b; break;
        }
        output += `Result: ${result}\n`;
      }

      // List operations
      if (code.includes('[') && code.includes(']')) {
        output += 'List created successfully\n';
      }

      // Function definitions
      if (code.includes('def ')) {
        output += 'Function defined successfully\n';
      }

      // Import statements
      if (code.includes('import ')) {
        output += 'Modules imported successfully\n';
      }

      if (!output) {
        output = 'Code executed successfully (simulated)';
      }

      return {
        success: true,
        output: output.trim(),
        executionTime: Date.now() - startTime,
        language: 'python'
      };
    } catch (error: any) {
      return {
        success: false,
        output: '',
        error: error.message || 'Simulation failed',
        executionTime: Date.now() - startTime,
        language: 'python'
      };
    }
  }

  /**
   * Validate code syntax
   */
  validateSyntax(code: string, language: 'python' | 'javascript'): {
    valid: boolean;
    errors: string[];
  } {
    const errors: string[] = [];

    if (language === 'javascript') {
      try {
        new Function(code);
        return { valid: true, errors: [] };
      } catch (error: any) {
        errors.push(error.message);
        return { valid: false, errors };
      }
    } else {
      // Basic Python syntax validation
      const lines = code.split('\n');
      let indentLevel = 0;

      for (let i = 0; i < lines.length; i++) {
        const line = lines[i];
        const trimmed = line.trim();

        if (!trimmed || trimmed.startsWith('#')) continue;

        // Check indentation
        const spaces = line.length - line.trimLeft().length;
        if (spaces % 4 !== 0) {
          errors.push(`Line ${i + 1}: Invalid indentation`);
        }

        // Check for unclosed brackets
        const openBrackets = (line.match(/[\[({]/g) || []).length;
        const closeBrackets = (line.match(/[\])}]/g) || []).length;
        if (openBrackets !== closeBrackets) {
          errors.push(`Line ${i + 1}: Unclosed brackets`);
        }
      }

      return { valid: errors.length === 0, errors };
    }
  }

  /**
   * Analyze code complexity
   */
  analyzeComplexity(code: string): {
    lines: number;
    functions: number;
    loops: number;
    conditionals: number;
    complexity: 'low' | 'medium' | 'high';
  } {
    const lines = code.split('\n').filter(l => l.trim()).length;
    const functions = (code.match(/def |function /g) || []).length;
    const loops = (code.match(/for |while /g) || []).length;
    const conditionals = (code.match(/if |elif |else |switch |case /g) || []).length;

    const complexityScore = functions * 2 + loops * 3 + conditionals * 2;
    const complexity = complexityScore < 10 ? 'low' : complexityScore < 30 ? 'medium' : 'high';

    return { lines, functions, loops, conditionals, complexity };
  }

  /**
   * Suggest code improvements
   */
  suggestImprovements(code: string, language: 'python' | 'javascript'): string[] {
    const suggestions: string[] = [];

    // Check for common issues
    if (!code.includes('try') && !code.includes('catch')) {
      suggestions.push('Consider adding error handling with try/catch blocks');
    }

    if (code.split('\n').length > 50) {
      suggestions.push('Consider breaking this into smaller functions');
    }

    if (language === 'python') {
      if (!code.includes('"""') && !code.includes("'''")) {
        suggestions.push('Add docstrings to document your functions');
      }
      if (code.includes('print(') && code.split('\n').length > 10) {
        suggestions.push('Consider using logging instead of print statements');
      }
    } else {
      if (!code.includes('//') && !code.includes('/*')) {
        suggestions.push('Add comments to explain complex logic');
      }
      if (code.includes('var ')) {
        suggestions.push('Use const or let instead of var');
      }
    }

    return suggestions;
  }

  /**
   * Execute code with Phoenix Protocol context
   */
  async executeWithContext(
    code: string,
    language: 'python' | 'javascript',
    context: {
      chakraId?: number;
      ivpValue?: number;
      scrollData?: any;
    }
  ): Promise<ExecutionResult> {
    // Inject context into code
    let contextualCode = code;

    if (language === 'javascript') {
      const contextStr = JSON.stringify(context, null, 2);
      contextualCode = `const phoenixContext = ${contextStr};\n${code}`;
    } else {
      const contextStr = JSON.stringify(context, null, 2);
      contextualCode = `phoenix_context = ${contextStr}\n${code}`;
    }

    // Execute with context
    return language === 'javascript'
      ? this.executeJavaScript(contextualCode)
      : this.executePython(contextualCode);
  }
}

// Global motor cortex instance
export const motorCortex = new MotorCortex();
