#!/bin/bash
make install && psql -a -d postgres://dbname_r03l_user:hmGvZtlkNuh0o5OOxs8rYOLNTwTKVr22@dpg-cougrrud3nmc73adm41g-a.oregon-postgres.render.com/dbname_r03l -f database.sql
