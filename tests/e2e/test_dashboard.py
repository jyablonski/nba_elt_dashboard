from __future__ import annotations

import pytest
from selenium.common.exceptions import ElementClickInterceptedException
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait


pytestmark = pytest.mark.e2e
E2E_WAIT_TIMEOUT = 30


def _wait_timeout(dash_duo) -> int:
    return max(dash_duo.wait_timeout, E2E_WAIT_TIMEOUT)


def _wait_visible(dash_duo, selector: str):
    def find_visible(driver):
        for element in driver.find_elements(By.CSS_SELECTOR, selector):
            if element.is_displayed():
                return element
        return False

    return WebDriverWait(dash_duo.driver, _wait_timeout(dash_duo)).until(find_visible)


def _wait_for_visible_text(dash_duo, selector: str, expected: str):
    def has_expected_text(driver):
        elements = driver.find_elements(By.CSS_SELECTOR, selector)
        for element in elements:
            if element.is_displayed() and expected in element.text:
                return element
        return False

    return WebDriverWait(dash_duo.driver, _wait_timeout(dash_duo)).until(has_expected_text)


def _wait_for_nonempty_text(dash_duo, selector: str):
    def has_text(driver):
        element = driver.find_element(By.CSS_SELECTOR, selector)
        if element.is_displayed() and element.text.strip():
            return element
        return False

    return WebDriverWait(dash_duo.driver, _wait_timeout(dash_duo)).until(has_text)


def _inner_html(dash_duo, selector: str) -> str:
    return dash_duo.find_element(selector).get_attribute("innerHTML")


def _wait_for_html_change(dash_duo, selector: str, previous_html: str):
    def has_changed(driver):
        current_html = driver.find_element(By.CSS_SELECTOR, selector).get_attribute("innerHTML")
        return current_html if current_html != previous_html else False

    return WebDriverWait(dash_duo.driver, _wait_timeout(dash_duo)).until(has_changed)


def _click_element(dash_duo, element) -> None:
    dash_duo.driver.execute_script(
        "arguments[0].scrollIntoView({block: 'center', inline: 'nearest'});", element
    )
    try:
        element.click()
    except ElementClickInterceptedException:
        dash_duo.driver.execute_script("arguments[0].click();", element)


def _select_dcc_dropdown(
    dash_duo, selector: str, *, value: str | None = None, index: int | None = None
):
    dropdown = dash_duo.find_element(selector)
    control = dropdown.find_element(By.CSS_SELECTOR, ".Select-control")
    _click_element(dash_duo, control)

    def find_menu(driver):
        menus = dropdown.find_elements(By.CSS_SELECTOR, "div.Select-menu-outer")
        for menu in menus:
            if menu.is_displayed():
                return menu
        return False

    menu = WebDriverWait(dash_duo.driver, _wait_timeout(dash_duo)).until(find_menu)
    options = menu.find_elements(By.CSS_SELECTOR, "div.VirtualizedSelectOption")
    if isinstance(index, int):
        option = options[index]
    else:
        option = next((option for option in options if option.text == value), None)
        if option is None:
            raise AssertionError(f"Could not find dropdown option {value!r}")
    _click_element(dash_duo, option)


def _active_tab_text(driver) -> str:
    for link in driver.find_elements(By.CSS_SELECTOR, "#tabs a"):
        parent = link.find_element(By.XPATH, "..")
        link_classes = link.get_attribute("class") or ""
        parent_classes = parent.get_attribute("class") or ""
        is_active = (
            link.get_attribute("aria-selected") == "true"
            or "active" in link_classes.split()
            or "active" in parent_classes.split()
        )
        if is_active:
            return link.text.strip()
    return ""


def _click_tab(dash_duo, label: str) -> None:
    tabs = dash_duo.find_element("#tabs")
    for link in tabs.find_elements(By.CSS_SELECTOR, "a"):
        if link.text.strip().startswith(label):
            _click_element(dash_duo, link)
            WebDriverWait(dash_duo.driver, _wait_timeout(dash_duo)).until(
                lambda driver: _active_tab_text(driver).startswith(label)
            )
            return
    raise AssertionError(f"Could not find dashboard tab {label!r}")


def _start_dashboard(dash_duo, dashboard_app) -> None:
    dash_duo.start_server(dashboard_app)
    _wait_visible(dash_duo, "#tabs")


def test_all_dashboard_tabs_render(dash_duo, dashboard_app):
    _start_dashboard(dash_duo, dashboard_app)

    tab_content = {
        "Overview": "#player-scoring-efficiency-table",
        "Recent Games": "#recent-games-card-strip .recent-games-card",
        "Team Analysis": "#team-selector",
        "Schedule": "#schedule-table-selector",
        "Social Media Analysis": "#social-media-team-selector",
        "About": "h1.app-hero-title",
    }

    for label, selector in tab_content.items():
        _click_tab(dash_duo, label)
        _wait_visible(dash_duo, selector)

    _wait_for_visible_text(dash_duo, "h1.app-hero-title", "About This Project")


def test_overview_filter_updates_player_value_chart(dash_duo, dashboard_app):
    _start_dashboard(dash_duo, dashboard_app)

    _wait_visible(dash_duo, "#player-scoring-efficiency-table")
    _wait_visible(dash_duo, "#team-ratings-plot .js-plotly-plot")
    _wait_visible(dash_duo, "#player-value-analysis-plot .js-plotly-plot")

    previous_html = _inner_html(dash_duo, "#player-value-analysis-plot")
    _select_dcc_dropdown(dash_duo, "#player-value-team-filter", value="BOS")
    _wait_for_html_change(dash_duo, "#player-value-analysis-plot", previous_html)


def test_schedule_controls_update_table_and_plot(dash_duo, dashboard_app):
    _start_dashboard(dash_duo, dashboard_app)

    _click_tab(dash_duo, "Schedule")
    _wait_visible(dash_duo, "#schedule-table .schedule-tonight-card")
    _wait_visible(dash_duo, "#schedule-plot .js-plotly-plot")

    _select_dcc_dropdown(dash_duo, "#schedule-table-selector", value="Full Schedule")
    _wait_visible(dash_duo, "#schedule-full-table")

    previous_html = _inner_html(dash_duo, "#schedule-plot")
    _select_dcc_dropdown(
        dash_duo, "#schedule-plot-selector", value="Team Comebacks Analysis (Regular Season)"
    )
    _wait_for_html_change(dash_duo, "#schedule-plot", previous_html)


def test_team_selection_updates_analysis_outputs(dash_duo, dashboard_app):
    _start_dashboard(dash_duo, dashboard_app)

    _click_tab(dash_duo, "Team Analysis")
    _wait_visible(dash_duo, "#team-selector")
    _wait_visible(dash_duo, "#mov-plot .js-plotly-plot")

    previous_html = _inner_html(dash_duo, "#mov-plot")
    _select_dcc_dropdown(dash_duo, "#team-selector", value="Los Angeles Lakers")
    _wait_for_visible_text(dash_duo, "#team-selector .Select-value-label", "Los Angeles Lakers")
    _wait_for_visible_text(dash_duo, "#kpi-boxes-1", "Team ratings")
    _wait_for_nonempty_text(dash_duo, "#team-payroll-value")
    _wait_for_html_change(dash_duo, "#mov-plot", previous_html)


def test_recent_game_selection_updates_play_by_play_chart(dash_duo, dashboard_app):
    _start_dashboard(dash_duo, dashboard_app)

    _click_tab(dash_duo, "Recent Games")
    _wait_visible(dash_duo, "#recent-games-card-strip .recent-games-card")
    _wait_visible(dash_duo, "#pbp-analysis-plot .js-plotly-plot")

    previous_html = _inner_html(dash_duo, "#pbp-analysis-plot")

    def find_game_cards(driver):
        cards = driver.find_elements(By.CSS_SELECTOR, "#recent-games-card-strip .recent-games-card")
        visible_cards = [card for card in cards if card.is_displayed()]
        return visible_cards if len(visible_cards) > 1 else False

    cards = WebDriverWait(dash_duo.driver, _wait_timeout(dash_duo)).until(find_game_cards)
    _click_element(dash_duo, cards[1])
    _wait_for_html_change(dash_duo, "#pbp-analysis-plot", previous_html)


def test_social_team_selection_updates_sentiment_chart(dash_duo, dashboard_app):
    _start_dashboard(dash_duo, dashboard_app)

    _click_tab(dash_duo, "Social Media Analysis")
    _wait_visible(dash_duo, "#social-media-team-selector")
    _wait_visible(dash_duo, "#social-media-plot .js-plotly-plot")

    previous_html = _inner_html(dash_duo, "#social-media-plot")
    _select_dcc_dropdown(dash_duo, "#social-media-team-selector", value="GSW")
    _wait_for_html_change(dash_duo, "#social-media-plot", previous_html)
