from selenium import webdriver


# Class to create browser instances
class BrowserFactory:
    """Factory para crear instancias de navegadores en modo headless."""
    @staticmethod
    def get_browser(browser_name):
        if browser_name.lower() == "chrome":
            options = webdriver.ChromeOptions()
            options.add_argument("--headless")  # Headless mode for Chrome
            return webdriver.Chrome(options=options)
        elif browser_name.lower() == "edge":
            options = webdriver.EdgeOptions()
            options.add_argument("--headless")  # Headless mode for Edge
            return webdriver.Edge(options=options)
        elif browser_name.lower() == "firefox":
            options = webdriver.FirefoxOptions()
            options.add_argument("--headless")  # Headless mode for Firefox
            return webdriver.Firefox(options=options)
        else:
            raise ValueError(f"Navegador no soportado: {browser_name}")

