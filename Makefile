build:
	python -m venv ./rpilocatorEnv
	./rpilocatorEnv/bin/pip install -r requirements.txt

clean:
	deactivate || true
	rm -rf ./rpilocatorEnv
