*** Settings ***
Documentation                                                  Variables and keywords for new registration
Library                                                        SeleniumLibrary
Resource                                                       ../PageObject/Generic.robot


*** Variables ***
${REGISTER_BUTTON}                                          xpath:/html/body/nav/ul/li[1]/a
${USERNAME_FIELD}                                           id:username
${PASSWORD_FIELD}                                           id:password
${FIRSTNAME_FIELD}                                          name:firstname
${LASTNAME_FIELD}                                           name:lastname
${PHONENUMBER_FIELD}                                        name:phone
${REGISTER_BTN}                                             css:form input[type='submit']
${USERNAME}                                                 ${EMPTY}
${PASSWORD}                                                 ${EMPTY}



*** Keywords ***
Create username and password for new user
            [Arguments]
            Wait and click element                   ${REGISTER_BUTTON}
            Wait and input text                      ${USERNAME_FIELD}              ${USERNAME}
            Wait and input text                      ${PASSWORD_FIELD}              ${PASSWORD}

Enter first and last name
            Wait and input text                      ${FIRSTNAME_FIELD}             Sulaimon
            Wait and input text                      ${LASTNAME_FIELD}              Ekundayo

Enter phone number and click register button
            Wait and input text                      ${PHONENUMBER_FIELD}           +358441121212
            Wait and click element                   ${REGISTER_BTN}
