import os
from log_analyzer_tool import LogAnalyzerTool

def main():
    # Initialize the log analyzer with model-only approach (default)
    analyzer = LogAnalyzerTool()
    
    # Analyze logs
    results = analyzer.analyze_csv('test_data/sample_logs.csv')
    
    # Save results to JSON
    analyzer.save_to_json(results, 'test_data/analysis_results.json')
    
    # Save results to database
    analyzer.save_to_database(results)
    
    # Print summary
    anomaly_count = sum(1 for r in results if r['status'] == 'anomaly')
    print(f'Analysis complete: {len(results)} logs processed, {anomaly_count} anomalies detected')

if __name__ == '__main__':
    main()
