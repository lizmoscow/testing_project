import React, {Component} from "react";
import {Grid, Button, Typography} from "@material-ui/core";
import CreateRoomPage from "./CreateRoomPage";

export default class Room extends Component {
    constructor(props) {
        super(props);
        this.state = {
            votesToSkip: 2,
            guestCanPause: false,
            isHost: false,
            showSettings: false,
            NoHost: true,
        };
        this.roomCode = this.props.match.params.roomCode;
        this.getRoomDetails();
        this.getRoomDetails = this.getRoomDetails.bind(this);
        this._leaveButtonPressed = this._leaveButtonPressed.bind(this);
        this._updateShowSettings = this._updateShowSettings.bind(this);
        this._renderSettings = this._renderSettings.bind(this);
        this._renderSettingsButton = this._renderSettingsButton.bind(this);
        this._host = this._host.bind(this);
    }

    getRoomDetails() {
         const requestOptions = {
            method: "GET",
            credentials: 'omit',
        };
        fetch("/api/get_room" + "?code=" + this.roomCode, requestOptions)
            .then((response) => {
                if (!response.ok) {
                    this.props.leaveRoomCallback();
                    this.props.history.push("/");
                }
                return response.json();
            })
            .then((data) => {
                this.setState({
                    votesToSkip: data.votes_to_skip,
                    guestCanPause: data.guest_can_pause,
                    isHost: data.is_host,
                });
        });
    }

    _leaveButtonPressed() {
        const requestOptions = {
            method: "POST",
            credentials: 'omit',
            headers: {"Content-Type": "application/json"},
        };
        fetch('/api/leave_room', requestOptions)
            .then((_response) => {
                this.props.leaveRoomCallback();
                this.props.history.push('/')
            });
    }

    _updateShowSettings(value) {
        this.setState({
            showSettings: value,
        });
    }

    _renderSettings() {
        return (<Grid container spacing={1}>
            <Grid item xs={12} align="center">
                <CreateRoomPage
                    update={true}
                    votesToSkip={this.state.votesToSkip}
                    guestCanPause={this.state.guestCanPause}
                    roomCode={this.roomCode}
                    updateCallback={this.getRoomDetails}/>
            </Grid>
            <Grid item xs={12} align="center">
                <Button variant="contained"
                      color="secondary"
                      onClick={() => this._updateShowSettings(false)}>
                    Close
                </Button>
            </Grid>
        </Grid>);
    }

    _renderSettingsButton() {
        return (
          <Grid item xs={12} align="center">
              <Button variant="contained"
                      color="primary"
                      onClick={() => this._updateShowSettings(true)}>
                  Settings
              </Button>
          </Grid>
        );
    }

    _host() {
        <Grid item xs={12} align="center">
                    <Typography variant="h6" component="h6">
                        Host: {this.state.isHost.toString()}
                    </Typography>
                </Grid>
    }

    render() {
        if (this.state.showSettings) {
            return this._renderSettings();
        }
        return (
            <Grid container spacing={1}>
                <Grid item xs={12} align="center">
                    <Typography variant="h4" component="h4" name={"code"}>
                        Code: {this.roomCode}
                    </Typography>
                </Grid>
                <Grid item xs={12} align="center">
                    <Typography variant="h6" component="h6" name="votes">
                        Votes: {this.state.votesToSkip}
                    </Typography>
                </Grid>
                <Grid item xs={12} align="center">
                    <Typography variant="h6" component="h6" name="pause">
                        Guest Can Pause: {this.state.guestCanPause.toString()}
                    </Typography>
                </Grid>
                {!this.NoHost ? this._host() : ""}
                {this.state.isHost ? this._renderSettingsButton() : null}
                <Grid item xs={12} align="center">
                    <Button color="secondary"
                            variant="contained"
                    onClick={this._leaveButtonPressed} name="leave">
                        Leave Room
                    </Button>
                </Grid>
            </Grid>
            );
    }
}