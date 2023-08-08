#This is a temporary script to test the scripts in the examples directory


from sys import argv


script_name = argv[1]
exec(f"from examples import {script_name}")
exec(f"{script_name}.main()")