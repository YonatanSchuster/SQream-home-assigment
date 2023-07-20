class Queries:
    tpch_queries = {
        "tpch5": "SELECT n_name, sum(l_extendedprice * (1 - l_discount)) AS revenue "
                 "FROM customer, orders, lineitem, supplier, nation, region "
                 "WHERE c_custkey = o_custkey AND l_orderkey = o_orderkey AND l_suppkey = s_suppkey "
                 "AND c_nationkey = s_nationkey AND s_nationkey = n_nationkey AND n_regionkey = r_regionkey "
                 "AND r_name = 'ASIA' AND o_orderdate >= '1994-01-01' AND o_orderdate < '1995-01-01' "
                 "GROUP BY n_name "
                 "ORDER BY revenue DESC;",
        "tpch7": "SELECT n1.n_name AS supp_nation, n2.n_name AS cust_nation, "
                 "extract(year FROM l_shipdate) AS l_year, sum(l_extendedprice * (1 - l_discount)) AS revenue "
                 "FROM supplier, lineitem, orders, customer, nation n1, nation n2 "
                 "WHERE s_suppkey = l_suppkey AND o_orderkey = l_orderkey "
                 "AND c_custkey = o_custkey AND s_nationkey = n1.n_nationkey "
                 "AND c_nationkey = n2.n_nationkey AND ( "
                 "    (n1.n_name = 'FRANCE' AND n2.n_name = 'GERMANY') "
                 "    OR (n1.n_name = 'GERMANY' AND n2.n_name = 'FRANCE') "
                 ") AND l_shipdate BETWEEN '1995-01-01' AND '1996-12-31' "
                 "GROUP BY supp_nation, cust_nation, l_year "
                 "ORDER BY supp_nation, cust_nation, l_year;"
    }

    select_query = "SELECT run_datetime, tpch_query_name, benchmark_result FROM tpch_results;"
    delete_customer_query = "DELETE FROM customer;"
    create_table_query = '''
        CREATE TABLE IF NOT EXISTS %s (
            run_datetime TIMESTAMP,
            tpch_query_name TEXT,
            benchmark_result NUMERIC
        );
        '''

    insert_query = "INSERT INTO tpch_results (run_datetime, tpch_query_name, benchmark_result) VALUES (%s, %s, %s);"
