import React, {Component} from "react";
import {TextField, Button, Grid, Typography} from "@material-ui/core";
import {Link} from "react-router-dom";


export  default class RoomJoinPage extends Component {
    constructor(props) {
        super(props);
        let token = localStorage.getItem('key');
        token = (token == null) ? "" : token;
        this.state = {
          roomCode: "",
          error: "",
            token: token,
        };
        this._handleTextFieldChange = this._handleTextFieldChange.bind(this);
        this._roomButtonPressed = this._roomButtonPressed.bind(this);
    }

    render() {
        return (
            <Grid container spacing={1}>
                <Grid item xs={12} align="center">
                    <Typography variant="h4" component="h4" id="page-title">
                        Join a Room
                    </Typography>
                </Grid>
                <Grid item xs={12} align="center">
                    <TextField
                        error={this.state.error.length > 0}
                        label="Code"
                        placeholder="Enter a Room Code"
                        value={this.state.roomCode}
                        helperText={this.state.error}
                        variant="outlined"
                        onChange={this._handleTextFieldChange}
                        name="roomName"
                    />
                </Grid>
                <Grid item xs={12}  align="center">
                    <Button variant="contained" color="primary" onClick={this._roomButtonPressed} name="enter">
                        Enter Room
                    </Button>
                </Grid>
                <Grid item xs={12}  align="center">
                    <Button variant="contained" color="secondary" to="/" component={Link} id="back">
                        Back
                    </Button>
                </Grid>
            </Grid>
        );
    }

    _handleTextFieldChange(e) {
        this.setState({
            roomCode: e.target.value
        });
    }

    _roomButtonPressed() {
        const requestOptions = {
            method: "POST",
            //credentials: 'omit',
            headers: {"Content-Type": "application/json",
                "Authorization": "Token " +  this.state.token},
            body: JSON.stringify({
                code: this.state.roomCode,
            }),
        };
        fetch("/api/join_room", requestOptions)
            .then((response) => {
            if (response.ok) {
                this.props.history.push(`/room/${this.state.roomCode}`);
            }
            else {
                this.setState({
                    error: "Room is unavailable"
                });
            }
        }).catch((error) => { console.log(code); });
    }
}