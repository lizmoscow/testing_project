describe('Check main functionality', () => {

    it('Loads successfully', () => {
        cy.visit('http://127.0.0.1:8000/')
        cy.contains('House Party')

        cy.contains('Join a Room').click()
        cy.url().should('include', 'join')
        cy.contains('Back').click()

        cy.contains('Create a Room').click()
        cy.url().should('include', 'create')
        cy.contains('Back').click()

        cy.contains('Log in').click()
        cy.url().should('include', 'login')
        cy.contains('Back').click()

    })

    it('Can log in successfully', () => {
        cy.visit('http://127.0.0.1:8000/login')
        cy.contains('Sign In')

        const username = Math.random().toString(36).substr(2, 7)
        const password = Math.random().toString(36).substr(2, 8)
        cy.get('input[name="username"]').type(username)
        cy.get('input[name="password"]').type(password)

        cy.get('button[name="switch"]').click()
        cy.get('button[name="signin"]').click()
        cy.contains('Signed up in successfully')
        cy.contains('Back').click()

        cy.contains('House Party with ' + username)
        cy.contains('Log out').click()
        cy.contains('House Party')

        cy.contains('Log in').click()

        cy.get('input[name="username"]').type(username)
        cy.get('input[name="password"]').type(password)
        cy.get('button[name="signin"]').click()
        cy.contains('House Party with ' + username)
        cy.contains('Log out').click()
    })

    it('Can join a room successfully', () => {
        cy.visit('http://127.0.0.1:8000/join')
        cy.contains('Join a Room')
        cy.get('input[name="roomName"]').type('ABCDEF')
        cy.contains('Enter Room').click()

        cy.contains('ABCDEF')
        cy.contains('Leave Room').click()
        cy.contains('House Party')

    })

    it('Can create a room successfully', () => {
        cy.visit('http://127.0.0.1:8000/create')
        cy.contains('Create a Room')
        cy.get('[type="radio"]').last().check()
        cy.get('input[name="NumOfVotes"]').type('6')
        cy.get('button').contains('Create a Room').click()

        cy.contains('Room')
        cy.contains('false')
        cy.contains('6')
        cy.contains('Leave Room').click()
        cy.contains('House Party')

    })

})