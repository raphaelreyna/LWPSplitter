#! /bin/bash

function execute_all_sql {
	for file in ./*.sql; do
		psql lwp_roots < $file
	done
}

cd functions && execute_all_sql
cd ./admin && execute_all_sql
cd ../../tables && execute_all_sql
cd ../views && execute_all_sql
