import sys
from PyQt5.QtCore import *
from PyQt5.QtGui import QKeySequence
from PyQt5.QtWidgets import *
from PyQt5.QtWebEngineWidgets import *


class InPrivateProfile(QWebEngineProfile):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setHttpCacheType(QWebEngineProfile.NoCache)
        self.setPersistentCookiesPolicy(QWebEngineProfile.NoPersistentCookies)


class InPrivateTab(QWebEngineView):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.setAttribute(Qt.WA_DeleteOnClose)
        self.setUrl(QUrl("https://www.google.com/"))
        profile = InPrivateProfile(self)
        self.setPage(QWebEnginePage(profile, self))


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.tabs = QTabWidget()
        self.tabs.setTabsClosable(True)
        self.tabs.tabCloseRequested.connect(self.close_current_tab)
        self.tabs.currentChanged.connect(self.current_tab_changed)
        self.setCentralWidget(self.tabs)
        


        self.add_new_tab(QUrl('http://qmamu.com'), 'Homepage')

        # navbar
        navbar = QToolBar()
        self.addToolBar(navbar)

        back_btn = QAction('Back', self)
        back_btn.triggered.connect(self.current_browser.back)
        navbar.addAction(back_btn)

        forward_btn = QAction('Forward', self)
        forward_btn.triggered.connect(self.current_browser.forward)
        navbar.addAction(forward_btn)

        reload_btn = QAction('Reload', self)
        reload_btn.triggered.connect(self.current_browser.reload)
        navbar.addAction(reload_btn)

        home_btn = QAction('Home', self)
        home_btn.triggered.connect(self.navigate_home)
        navbar.addAction(home_btn)

        self.url_bar = QLineEdit()
        self.url_bar.returnPressed.connect(self.navigate_to_url)
        navbar.addWidget(self.url_bar)

        new_tab_btn = QAction('New Tab', self)
        new_tab_btn.setShortcut(QKeySequence("Ctrl+T"))
        new_tab_btn.triggered.connect(self.add_new_tab_with_url_bar)
        navbar.addAction(new_tab_btn)

        close_tab_btn = QAction('Close Tab', self)
        close_tab_btn.setShortcut(QKeySequence("Ctrl+W"))
        close_tab_btn.triggered.connect(self.close_current_tab_shortcut)
        navbar.addAction(close_tab_btn)

        inprivate_tab_btn = QAction('New InPrivate Tab', self)
        inprivate_tab_btn.setShortcut(QKeySequence("Ctrl+Shift+N"))
        inprivate_tab_btn.triggered.connect(self.add_inprivate_tab)
        navbar.addAction(inprivate_tab_btn)

        # settings button
        settings_btn = QAction('Settings', self)
        settings_btn.triggered.connect(self.show_settings)
        navbar.addSeparator()
        navbar.addAction(settings_btn)

    def show_settings(self):
        settings_dialog = QDialog(self)
        settings_dialog.setWindowTitle('Settings')
        settings_dialog.exec_()

    def add_new_tab(self, qurl=None, label="Blank"):
        if qurl is None:
            qurl = QUrl('https://www.google.com/')
        browser = QWebEngineView()
        browser.setUrl(qurl)
        i = self.tabs.addTab(browser, label)
        self.tabs.setCurrentIndex(i)
        browser.urlChanged.connect(lambda qurl, browser=browser:
                                   self.update_url_bar(qurl, browser))
        browser.loadFinished.connect(lambda _, i=i, browser=browser:
                                     self.tabs.setTabText(i, browser.page().title()))
        self.current_browser = browser

    def add_new_tab_with_url_bar(self):
        self.add_new_tab(QUrl(self.url_bar.text()), self.url_bar.text())

    def add_inprivate_tab(self):
        browser = InPrivateTab()
        i = self.tabs.addTab(browser, 'InPrivate Tab')
        self.tabs.setCurrentIndex(i)

    def close_current_tab(self, i):
        if self.tabs.count() < 2:
            return
        self.tabs.removeTab(i)


    def close_current_tab_shortcut(self):
        i = self.tabs.currentIndex()
        self.close_current_tab(i)

    def current_tab_changed(self, i):
        self.current_browser = self.tabs.widget(i)
        self.update_url_bar(self.current_browser.url(), self.current_browser)

    def update_url_bar(self, q, browser=None):
        if browser != self.current_browser:
            return
        self.url_bar.setText(q.toString())

    def navigate_home(self):
        self.current_browser.setUrl(QUrl('https://google.com'))

    def navigate_to_url(self):
        url = self.url_bar.text()
        if not url.startswith('http'):
            url = 'http://' + url
        q = QUrl(url)
        self.current_browser.setUrl(q)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    QApplication.setApplicationName('Gnikcah browzer')
    window = MainWindow()
    window.showMaximized()
    app.exec_()


