*** Settings ***
Documentation                                               A resource file with reusable keywords and variables
Library                                                     SeleniumLibrary
Library                                                     DriverManager.py



*** Variables ***
${URL}                                                      http://127.0.0.1:8080
${BROWSER}                                                  Chrome


*** Keywords ***
Open broswer with the url
            ${driver_path}=     Get Chrome Driver Path
            Open Browser        ${URL}      ${BROWSER}        executable_path=${driver_path}
            Maximize Browser Window

Wait and click element
            [arguments]         ${page_locator}
            Wait Until Element Is Visible        ${page_locator}        timeout=10
            Click Element    ${page_locator}

Wait and input text
            [Arguments]         ${page_locator}     ${text}
            Wait Until Element Is Visible               ${page_locator}        timeout=10
            Input Text                                  ${page_locator}      ${text}
