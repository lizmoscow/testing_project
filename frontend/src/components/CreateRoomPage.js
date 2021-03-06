import React, {Component} from "react";
import {Button} from "@material-ui/core";
import {Grid} from "@material-ui/core";
import {Typography} from "@material-ui/core";
import {TextField} from "@material-ui/core";
import {FormHelperText} from "@material-ui/core";
import {FormControl} from "@material-ui/core";
import {Link} from "react-router-dom";
import {Radio} from "@material-ui/core";
import {RadioGroup} from "@material-ui/core";
import {FormControlLabel} from "@material-ui/core";
import {Collapse} from "@material-ui/core";
import {Alert} from "@material-ui/lab";


export  default class CreateRoomPage extends Component {
    static defaultProps = {
        votesToSkip: 2,
        guestCanPause: true,
        update: false,
        roomCode: null,
        updateCallback: () => {},
        errorMsg: "",
        successMsg: "",
    };

    constructor(props) {
        super(props);
        let token = localStorage.getItem('key');
        token = (token == null) ? "" : token;
        this.state = {
            guestCanPause : this.props.guestCanPause,
            votesToSkip: this.props.votesToSkip,
            token: token,
            errorMsg: this.props.errorMsg,
            successMsg: this.props.successMsg,
        };
        this.handleRoomButtonPressed = this.handleRoomButtonPressed.bind(this);
        this.handleVotesChange = this.handleVotesChange.bind(this);
        this.handleGuestCanPauseChange = this.handleGuestCanPauseChange.bind(this);
        this._renderCreateButtons = this._renderCreateButtons.bind(this);
        this._renderUpdateButtons = this._renderUpdateButtons.bind(this);
        this._handleUpdateButtonPressed = this._handleUpdateButtonPressed.bind(this);
    }

    handleVotesChange(e) {
        this.setState({
            votesToSkip: e.target.value,
        });
    }

    handleGuestCanPauseChange(e) {
        this.setState({
            guestCanPause: e.target.value === "true",
        });
    }

    handleRoomButtonPressed() {
        const requestOptions = {
            method: "POST",
            //credentials: 'omit',
            headers: {"Content-Type": "application/json",
                "Authorization": "Token " + this.state.token},
            body: JSON.stringify({
                votes_to_skip: this.state.votesToSkip,
                guest_can_pause: this.state.guestCanPause,
            }),
        };
        fetch('/api/create_room', requestOptions)
            .then((response) => response.json())
            .then((data) => this.props.history.push('/room/' + data.code));
    }

    _renderCreateButtons() {
        return (
            <Grid container spacing={1}>
                <Grid item xs={12} align="center">
                    <Button color="primary"
                            variant="contained"
                            onClick={this.handleRoomButtonPressed}
                            name="create">
                        Create a Room
                    </Button>
                </Grid>
                <Grid item xs={12} align="center">
                    <Button color="secondary"
                            variant="contained"
                            to="/"
                            component={Link} id="back">
                        Back
                    </Button>
                </Grid>
            </Grid>
        );
    }

    _handleUpdateButtonPressed() {
        const requestOptions = {
            method: "PATCH",
            //credentials: 'omit',
            headers: {"Content-Type": "application/json",
                "Authorization": "Token " + this.state.token},
            body: JSON.stringify({
                votes_to_skip: this.state.votesToSkip,
                guest_can_pause: this.state.guestCanPause,
                code: this.props.roomCode
            }),
        };
        fetch('/api/update_room', requestOptions)
            .then((response) => {
                if (response.ok) {
                    this.setState({
                        successMsg: "Room updated successfully"
                    });
                }
                else {
                    this.setState({
                        errorMsg: "Error updating room"
                    });
                }
                this.props.updateCallback();
            });
    }

    _renderUpdateButtons() {
        return(
            <Grid item xs={12} align="center">
                    <Button color="primary"
                            variant="contained"
                            onClick={this._handleUpdateButtonPressed}>
                        Update the Room
                    </Button>
                </Grid>
        );
    }

    render() {
        const title = this.props.update ? "Update the Room" : "Create a Room";

        return <Grid container spacing={1}>
            <Grid item xs={12} align="center">
                <Collapse in={this.state.errorMsg.length > 0 || this.state.successMsg.length > 0}>
                    {this.state.successMsg
                        ? (<Alert severity="success"
                                  onClose={() => {
                                      this.setState({successMsg: ""});}
                                  }
                        >{this.state.successMsg}</Alert>)
                        : (<Alert severity="error"
                                  onClose={() => {
                                      this.setState({errorMsg: ""});}
                                  }
                        >{this.state.errorMsg}</Alert>)}
                </Collapse>
            </Grid>
            <Grid item xs={12} align="center">
                <Typography component='h4' variant='h4' id="page-title">
                    {title}
                </Typography>
            </Grid>
            <Grid item xs={12} align="center">
                <FormControl component="fieldset">
                    <FormHelperText>
                            Guest Control of Playback State
                    </FormHelperText>
                    <RadioGroup row defaultValue={this.state.guestCanPause.toString()}
                    onChange={this.handleGuestCanPauseChange}>
                        <FormControlLabel
                            value="true"
                            control={<Radio color="primary"/>}
                            label="Play/Pause"
                            labelPlacement="bottom"
                            name="giveGuestControl"/>
                        <FormControlLabel
                            value="false"
                            control={<Radio color="secondary"/>}
                            label="No Control"
                            labelPlacement="bottom"
                            name="refuseGuestControl"/>
                    </RadioGroup>
                </FormControl>
            </Grid>
            <Grid item xs={12} align="center">
                <FormControl>
                    <TextField required={true}
                               type="number"
                               onChange={this.handleVotesChange}
                               defaultValue={this.state.votesToSkip}
                               inputProps={{
                                   min: 1,
                                   style: {textAlign: "center"}
                               }}
                               data-testid="NumOfVotes"
                               name="NumOfVotes"
                    />
                    <FormHelperText>
                            Votes Required to Skip
                    </FormHelperText>
                </FormControl>
            </Grid>
            {this.props.update ? this._renderUpdateButtons() : this._renderCreateButtons()}
        </Grid>;
    }
}