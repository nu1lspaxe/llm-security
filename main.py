from data_collection.log_collector import LogCollector
from data_collection.data_processor import DataProcessor

def main():
    collector = LogCollector(log_file="/var/log/syslog")
    processor = DataProcessor()

    try:
        for log_line in collector.collect_logs():
            processed_log = processor.process_log(log_line)
            if processed_log:
                processor.add_to_vector_db(processed_log)

            if len(processor.logs) % 10 == 0:
                response = processor.query("What issues are occurring?")
                print(f"Response: {response}")
            
    except KeyboardInterrupt:
        exit(0)

if __name__ == "__main__":
    main()