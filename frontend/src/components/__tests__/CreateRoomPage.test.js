import React from 'react';
import { BrowserRouter } from 'react-router-dom';
import {fireEvent, render, screen} from '@testing-library/react';
import UserEvent from '@testing-library/user-event';
import CreateRoomPage from "../CreateRoomPage";

/**
 * @jest-environment jsdom
 */


describe('Testing CreateRoom Component when update=false', () => {
    test('page has a Create a Room title', () => {
      render(<BrowserRouter><CreateRoomPage/></BrowserRouter>);
      expect(screen.getAllByText('Create a Room')).toBeTruthy();
    });

    test('page does not have a Update the Room title', () => {
      render(<BrowserRouter><CreateRoomPage/></BrowserRouter>);
      expect(screen.queryByText('Update the Room')).toBeFalsy();
    });

    test('guest can pause is set to true', () => {
      render(<BrowserRouter><CreateRoomPage/></BrowserRouter>);
      const labelRadio1 = screen.getByLabelText('No Control');
      expect(labelRadio1.checked).toEqual(false);
      const labelRadio2 = screen.getByLabelText('Play/Pause');
      expect(labelRadio2.checked).toEqual(true);
    });

    test('votes to skip is equal to 2', () => {
      render(<BrowserRouter><CreateRoomPage/></BrowserRouter>);
      const form = screen.getByDisplayValue('2');
      expect(form).toBeTruthy();
    });
});


describe('Testing CreateRoom Component when update=false', () => {
    test('page does not have a Create a Room title', () => {
      render(<BrowserRouter><CreateRoomPage
        votesToSkip={6}
        guestCanPause={false}
        update={true} /></BrowserRouter>);
      expect(screen.queryByText('Create a Room')).toBeFalsy();
    });

    test('page does have a Update the Room title', () => {
      render(<BrowserRouter><CreateRoomPage
        votesToSkip={6}
        guestCanPause={false}
        update={true} /></BrowserRouter>);
      expect(screen.getAllByText('Update the Room')).toBeTruthy();
    });

    test('guest can pause is set to false', () => {
      render(<BrowserRouter><CreateRoomPage
        votesToSkip={6}
        guestCanPause={false}
        update={true} /></BrowserRouter>);
      const labelRadio1 = screen.getByLabelText('No Control');
      expect(labelRadio1.checked).toEqual(true);
      const labelRadio2 = screen.getByLabelText('Play/Pause');
      expect(labelRadio2.checked).toEqual(false);
    });

    test('votes to skip is equal to 2', () => {
      render(<BrowserRouter><CreateRoomPage
        votesToSkip={6}
        guestCanPause={false}
        update={true} /></BrowserRouter>);
      const form = screen.getByDisplayValue('6');
      expect(form).toBeTruthy();
    });
});