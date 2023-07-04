all		:	venv
			python3 main.py

env		:
			source venv/Scripts/activate

.PHONY	:	env