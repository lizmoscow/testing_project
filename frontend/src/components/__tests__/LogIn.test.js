import React from 'react';
import { BrowserRouter } from 'react-router-dom';
import {render, screen} from '@testing-library/react';
import UserEvent from '@testing-library/user-event';
import LogIn from "../LogIn";

/**
 * @jest-environment jsdom
 */


describe('Testing LogIn Component', () => {
    test('render Sing In page', () => {
      render(<BrowserRouter><LogIn/></BrowserRouter>);
      expect(screen.getAllByText('Sign In')).toBeTruthy();
    });

    test('render Sing In title', () => {
      render(<BrowserRouter><LogIn/></BrowserRouter>);
      const el = screen.getByTestId('Title');
      expect(el.textContent).toBe('Sign In');
    });

    test('render Sign Up page', () => {
      render(<BrowserRouter><LogIn signUp={true}/></BrowserRouter>);
      expect(screen.getAllByText('Sign Up')).toBeTruthy();
    });

    test('render Sign Up title', () => {
      render(<BrowserRouter><LogIn signUp={true}/></BrowserRouter>);
      const el = screen.getByTestId('Title');
      expect(el.textContent).toBe('Sign Up');
    });

    test('render Sign Up button', () => {
      render(<BrowserRouter><LogIn signUp={true}/></BrowserRouter>);
      const el = screen.getByTestId('LogInButton');
      expect(el.textContent).toBe('Sign Up');
    });

    test('render Sign in button', () => {
      render(<BrowserRouter><LogIn/></BrowserRouter>);
      const el = screen.getByTestId('LogInButton');
      expect(el.textContent).toBe('Sign In');
    });

    test('render switch mode button for Sign Up', () => {
      render(<BrowserRouter><LogIn signUp={true}/></BrowserRouter>);
      const el = screen.getByTestId('SwitchModeButton');
      expect(el.textContent).toBe('Already Have an Account?');
    });

    test('render switch mode button for Sign In', () => {
      render(<BrowserRouter><LogIn/></BrowserRouter>);
      const el = screen.getByTestId('SwitchModeButton');
      expect(el.textContent).toBe('Don\'t Have an Account Yet?');
    });

    test('switch mode button works', async () => {
      render(<BrowserRouter><LogIn/></BrowserRouter>);
      const title = screen.getByTestId('Title');
      expect(title.textContent).toBe('Sign In');
      const button = screen.getByTestId('SwitchModeButton');
      expect(button.textContent).toBe('Don\'t Have an Account Yet?');
      UserEvent.click(button);
      expect(title.textContent).toBe('Sign Up');
      expect(button.textContent).toBe('Already Have an Account?');
      UserEvent.click(button);
      expect(title.textContent).toBe('Sign In');
      expect(button.textContent).toBe('Don\'t Have an Account Yet?');
    });
});