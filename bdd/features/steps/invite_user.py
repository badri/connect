from behave import *


# Unique to Scenario: Moderator invites new user
@given('I invite a new user, with the name "First Last"')
def impl(context):
    context.execute_steps('''
        when I visit the "invite user" page
        when I enter "First" into the "first name" field
        when I enter "Last" into the "last name" field
        when I enter "new.user@test.test" into the "email" field
        when I submit the form
    ''')

@then('I see that the user has been added to my list of invitations pending activation')
def impl(context):
    assert context.browser.is_element_present_by_css('table.invitation-table', wait_time=5)
    assert context.browser.is_text_present('First Last', wait_time=5)
    assert context.browser.is_text_present('new.user@test.test', wait_time=5)
    assert context.browser.is_text_present('Resend Invitation', wait_time=5)
    assert context.browser.is_text_present('Revoke Invitation', wait_time=5)

