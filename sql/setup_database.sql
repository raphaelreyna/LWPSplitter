#! /bin/bash

function execute_all_sql {
	for file in ./*.sql; do
		psql lwp_roots < $file
	done
}

cd ./functions/admin && execute_all_sql
cd ../get && execute_all_sql
cd ../insert && execute_all_sql
cd ../state
cat get_max_degree.sql number_of_roots_logged_for_polynomial.sql | psql lwp_roots
execute_all_sql
cd ../../tables && execute_all_sql
cd ../views && execute_all_sql
