from selenium.common.exceptions import NoSuchElementException


def element_exists(driver, find_element_by, value):
    try:
        driver.find_element(by=find_element_by, value=value)
    except NoSuchElementException:
        return False
    return True
