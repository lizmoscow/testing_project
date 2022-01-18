# testing_project

This is a project for the software-testing course

gitPages: https://lizmoscow.github.io/testing_project/

the progect is deployed in https://software-testing-project.herokuapp.com/

### To run tests:

*   Backend tests: `python3 manage.py test`
	* Specific test case: `python3 manage.py test api.tests.<TestCaseName>`
	* Specific test: `python3 manage.py test api.tests.<TestCaseName>.<TestName>`
*   Frontend tests:
	* Component and e2e tests with Selenide: `npm run test`
	* e2e tests with Cypress: `npm run e2e`
	
### Tests that have yet to be written:

*	Component tests:
	 * Frontend:
	   * Home page (updating username, logging out, rendering buttons "Join Room", "Log in" / "Log out" and "Create a Room" depending on whether a user has been  authenticated or not)
	   * Room page (parsing request with room data, leaving room, rendering button "Settings" depending on who is viewing it)
	   * Room Join page (posting request to join the room and parsing the response) 
	 *	Backend:
		  * Room view test
		  * User view test
*	End-to-end tests:
	 * Editing a room
	 * Joining room as a host vs as a guest
	 * Trying to register with incorrect / already existing data
	 * Visiting pages Room, Create a Room, Edit the room as an unauthorised guest
	 	
### Test documentation 

Documentation for api module is located in file `api/documentation.md` generated with `inkpot` library


### Finished tasks

- [x] Lesson 2
  - [x] Main 
  - [x] Advanced 
  - [x] Bonus
- [ ] Lesson 4
  - [x] Main 
  - [x] Advanced 
  - [ ] Bonus
- [ ] Lesson 5
  - [x] Main 
  - [x] Advanced 
  - [ ] Bonus
- [ ] Lesson 6
  - [ ] Bonus
- [ ] Lesson 7
  - [ ] Bonus
- [ ] Lesson 8
  - [ ] Bonus
- [ ] Lesson 9
  - [x] Main 
  - [ ] Advanced 
  - [ ] Bonus
- [ ] Lesson 10
  - [ ] Main 
  - [ ] Advanced 
  - [ ] Bonus
