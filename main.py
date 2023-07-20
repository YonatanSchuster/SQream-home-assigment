import argparse
from tpch_util import create_schema, load_data, run_benchmark, fetch_results

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="TPCH Utility Script")
    parser.add_argument("--create_schema", action="store_true", help="Create TPCH schema")
    parser.add_argument("--load_data", action="store_true", help="Create TPCH schema")
    parser.add_argument("--run_benchmark", action="store_true", help="Create TPCH schema")
    parser.add_argument("--save_results", action="store_true", help="Create TPCH schema")
    parser.add_argument("--fetch_results", action="store_true", help="Create TPCH schema")




    args = parser.parse_args()

    if args.create_schema:
        create_schema()

    if args.load_data:
        load_data()

    if args.run_benchmark:
        run_benchmark(args)

    if args.fetch_results:
        fetch_results()
