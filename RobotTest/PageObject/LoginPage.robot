*** Settings ***
Documentation                                           Variables and keyords for login
Library                                                 SeleniumLibrary
Resource                                                ../PageObject/Generic.robot



*** Variables ***
${LOGIN_BUTTON}                                             xpath:/html/body/nav/ul/li[2]/a
${USERNAME_FIELD}                                           id:username
${PASSWORD_FIELD}                                           id:password
${SUBMIT_BUTTON}                                            css:form input[type='submit']
${USERNAME}                                                 tester2022
${PASSWORD}                                                 Tester@@4040



*** Keywords ***
Enter username and password
            [Arguments]
            Wait and click element                   ${LOGIN_BUTTON}
            Wait and input text                      ${USERNAME_FIELD}              ${USERNAME}
            Wait and input text                      ${PASSWORD_FIELD}              ${PASSWORD}
Click on submit button and close browser
            Wait and click element                   ${SUBMIT_BUTTON}
            Wait Until Page Contains                 User Information        timeout=10
            Close Browser