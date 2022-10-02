try
{
    python -m venv venv    # Creating virtual environment
    "+ Creating virtual environment"
    .\venv\Scripts\activate    # Activating virtual environment
    "+ Activating virtual environment"
    pip install -r requirements.txt    # Install packages
    "+ Install packages"

    python init_db.py    # Creating database
    "+ Creating database"

    python main.py    # Starting app
    "+ Starting app! Follow http://0.0.0.0:8000"
}
catch
{
    "⚠️ Error in line $($_.InvocationInfo.ScriptLineNumber): $($Error[0])"
	exit 1
}