describe('Check main functionality', () => {

    it('Can log in successfully', () => {
        cy.visit('http://127.0.0.1:8000/login')
        cy.contains('Sign In')

        cy.get('input[name="username"]').type("User")
        cy.get('input[name="password"]').type("password")

        cy.get('button[name="switch"]').click()
        cy.intercept('POST', '/api/token-reg/', {
            statusCode: 200,
            body: {
                username: 'User',
                token: '78cd2fcf9fdf3347846033400424429721858462',
            }
        });
        cy.get('button[name="signin"]').click()
        cy.contains('Signed up in successfully')
        cy.contains('Back').click()

        cy.contains('House Party with User')
        cy.contains('Log out').click()
        cy.contains('House Party')

        cy.contains('Log in').click()

        cy.get('input[name="username"]').type("User")
        cy.get('input[name="password"]').type("password")
        cy.intercept('POST', '/api/token-auth/', {
            statusCode: 200,
            body: {
                username: 'User',
                token: '78cd2fcf9fdf3347846033400424429721858462',
            }
        });
        cy.get('button[name="signin"]').click()
        cy.contains('House Party with User')
        cy.contains('Log out').click()
    })

    it('Loads successfully', () => {
        cy.visit('http://127.0.0.1:8000/')
        cy.contains('House Party')

        cy.contains('Log in').click()
        cy.url().should('include', 'login')
        cy.get('input[name="username"]').type("user")
        cy.get('input[name="password"]').type("password")

        cy.intercept('POST', '/api/token-auth/', {
            statusCode: 200,
            body: {
                username: 'user',
                token: '78cd2fcf9fdf3347846033400424429721858462',
            }
        });
        cy.get('button[name="signin"]').click()

        cy.contains('House Party with user')

        cy.contains('Join a Room').click()
        cy.url().should('include', 'join')
        cy.contains('Back').click()

        cy.contains('Create a Room').click()
        cy.url().should('include', 'create')
        cy.contains('Back').click()

        cy.contains('Log out').click()

    })

    it('Can create a room successfully', () => {
        cy.visit('http://127.0.0.1:8000/create')
        cy.contains('Create a Room')
        cy.get('[type="radio"]').last().check()
        cy.get('input[name="NumOfVotes"]').type('6')
        cy.intercept('POST', '/api/create_room', {
            statusCode: 200,
            body: {
                code: 'ABCDEF',
                guest_can_pause: 'False',
                votes_to_skip: '6',
            }
        });
        cy.intercept('GET', '/api/get_room?code=ABCDEF', {
            statusCode: 200,
            body: {
                code: 'ABCDEF',
                guest_can_pause: 'False',
                votes_to_skip: '6',
                is_host: "True"
            }
        });
        cy.get('button').contains('Create a Room').click()

        cy.contains('Room')
        cy.contains('false')
        cy.contains('ABCDEF')
        cy.contains('6')
        cy.contains('Leave Room').click()
        cy.contains('House Party')

    })

    it('Can join a room successfully', () => {
        cy.visit('http://127.0.0.1:8000/join')
        cy.contains('Join a Room')
        cy.get('input[name="roomName"]').type('ABCDEF')
        cy.intercept('POST', '/api/join_room', {
            statusCode: 200,
            body: {
                'Message' : 'Room Joined',
            }
        });
        cy.intercept('GET', '/api/get_room?code=ABCDEF', {
            statusCode: 200,
            body: {
                code: 'ABCDEF',
                guest_can_pause: 'False',
                votes_to_skip: '6',
                is_host: "True"
            }
        });
        cy.contains('Enter Room').click()

        cy.contains('ABCDEF')
        cy.contains('Leave Room').click()
        cy.contains('House Party')

    })

})