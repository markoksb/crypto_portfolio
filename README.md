# Cryptofolio
#### Video Demo TODO
#### Description
Cryptofolio: My CS50 2024 Final Project.
Cryptocurrency trading across multiple exchanges makes it challenging to track performance in a unified way. With coins often distributed across different exchanges and wallets, keeping track of them all can be confusing and may lead to missed opportunities.
I aimed to create an app to simplify tracking of cryptocurrencies across various platforms by aggregating data and providing real-time insights.<br>
For that reason, one can create multiple independent portfolios and add transactions to them. The app keeps track of profits and losses on a currency, portfolio, and user level.<br>
The app was built using Python, Flask, Jinja, JS, HTML, CSS, and SQLite. Additionally, Bootstrap for responsive design, the login_required decorator to secure access, and SQL wrapper introduced during the CS50 course.
While the initial version focuses on core functionality, future enhancements will include:
* Handling of various APIs and their keys to import data from exchanges.
* Blockchain integration to track non-exchange assets.
* The ability to conduct transactions right from the app.

These features will be part of future development, enhancing Cryptofolio's value beyond CS50.

#### Structure
```
cryptofolio/
├── static/                     # Contains static files like CSS, JS, images
│   ├── css/
│   │   └── main.css            # Main stylesheet
│   ├── img/
│   │   └── cross.png           # icon for portfolio deletion
│   └── favicon.ico             # favorite icon
├── templates/                  # HTML templates for Jinja rendering
│   ├── base.html               # Base template - html header, footer and navigation
│   ├── currencies.html         # Currency page - a table of the most important coins
│   ├── error.html              # Displays error messages #memegen
│   ├── index.html              # Homepage
│   ├── login.html              # User login form
│   ├── portfolio_cadd.html     # Form to add a coin to a portfolio
│   ├── portfolio_del.html      # Portfolio deletion form
│   ├── portfolio_new.html      # Portfolio creation form
│   ├── portfolio.html          # Portfolio page - Overview and portfolio subnav
│   └── register.html           # User registration form
├── app.py                      # Main Flask application - config and routing
├── cgecko.py                   # CoinGecko API implementations
├── currencies.py               # generates the coin list and updates its prices
├── database_schema.py          # strings to (re-)create the database
├── database.py                 # database functions
├── error.py                    # genrates error messages and char escapes
├── key.py                      # contains coingecko api key (not shared)
├── portfolio.db                # SQLite database file (example data)
├── portfolio.py                # aggregate and calculate data for each portfolio
├── README.md                   # Documentation file (this file)
├── req_login.py                # login_required decorator
├── requirements.txt            # Project dependencies
└── users.py                    # handling of user login/logout and registration
```

#### Challenges and Learning Outcomes
Effective project planning is crucial, yet even the most meticulously crafted plans can face unexpected hurdles. During the development of Cryptofolio, I encountered several challenges that required flexibility and quick problem-solving. External commitments often competed for my time and attention, requiring a balance between maintaining momentum on the project and fulfilling other responsibilities.<br>
Despite these challenges, this project has been an invaluable learning experience. I gained deeper insights into integrating different technologies, handling real-time data, and designing a user-centric application. I also learned to adapt my approach, troubleshoot unforeseen issues efficiently, and remain committed to continuous improvement.<br>
This project reinforced the importance of resilience and iterative progress. While the current version provides a solid foundation, I am eager to enhance and expand Cryptofolio as opportunities arise.

A notable technical challenge I faced was dealing with very small floating-point numbers. Tiny discrepancies can affect trust and insights. These small floats caused unexpected rounding errors or cluttered the user interface.<br>
To address this, I enhanced numerical precision in Jinja templates using custom formatting. Notably, I displayed them in scientific notation. This ensured consistent and readable outputs without excess digits.<br>
I learned the importance of precision in financial applications and refined my skills in data presentation and template rendering with Jinja. #memecoins

#### Contribute
Feel free to submit pull requests or report issues. :)

#### License
This project is licensed under the MIT License. This means you are free to use, copy, modify, and distribute the software, with the condition that the original license and copyright notice are included. The software is provided "as is," without any warranties, express or implied, including but not limited to merchantability or fitness for a particular purpose.

#### Credits
- **CoinGecko**: API for cryptocurrency data.
- **Flask**: Framework used for building the web app.
- **Bootstrap**: Frontend framework for responsive design.
- **CS50**: For providing the knowledge and skills needed to complete this project. This was CS50. 🦆
