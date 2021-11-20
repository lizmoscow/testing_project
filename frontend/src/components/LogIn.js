import React, {Component} from "react";
import {TextField, Button, Grid, Typography, Collapse} from "@material-ui/core";
import {Alert} from "@material-ui/lab";


export  default class LogIn extends Component {
    static defaultProps = {
        signUp: false,
    };

    constructor(props) {
        super(props);
        this.state = {
            error: "",
            username: "",
            password: "",
            errorMsg: "",
            successMsg: "",
            signUp: this.props.signUp,
        };
        this._handleUsernameTextFieldChange = this._handleUsernameTextFieldChange.bind(this);
        this._handlePasswordTextFieldChange = this._handlePasswordTextFieldChange.bind(this);
        this._loginButtonPressed = this._loginButtonPressed.bind(this);
        this._optionButtonPressed = this._optionButtonPressed.bind(this);
        this._backButtonPressed = this._backButtonPressed.bind(this);
    }

    render() {
        return (
            <Grid container spacing={1}>
                <Grid item xs={12} align="center">
                <Collapse in={this.state.errorMsg.length > 0 || this.state.successMsg.length > 0} data-testid="Message" id="message">
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
                    <Typography variant="h4" component="h4" data-testid="Title" id="page-title">
                        {(!this.state.signUp) ? "Sign In" : "Sign Up"}
                    </Typography>
                </Grid>
                <Grid item xs={12} align="center">
                    <TextField
                        error={this.state.error.length > 0}
                        label="Username"
                        placeholder="Enter a username"
                        value={this.state.username}
                        variant="outlined"
                        onChange={this._handleUsernameTextFieldChange}
                        data-testid="UsernameField"
                        name="username"
                    />
                </Grid>
                <Grid item xs={12} align="center">
                    <TextField
                        error={this.state.error.length > 0}
                        label="Password"
                        placeholder="Enter a password"
                        value={this.state.password}
                        variant="outlined"
                        type="password"
                        onChange={this._handlePasswordTextFieldChange}
                        name="password"
                    />
                </Grid>
                <Grid item xs={12}  align="center">
                    <Button
                        variant="contained"
                        color="primary"
                        onClick={this._loginButtonPressed}
                        data-testid="LogInButton"
                        name="signin">
                        {(!this.state.signUp) ? "Sign In" : "Sign Up"}
                    </Button>
                </Grid>
                <Grid item xs={12}  align="center">
                    <Button
                        variant="contained"
                        color="primary"
                        onClick={this._optionButtonPressed}
                        data-testid="SwitchModeButton"
                        name="switch">
                        {(!this.state.signUp) ? "Don't Have an Account Yet?" : "Already Have an Account?"}
                    </Button>
                </Grid>
                <Grid item xs={12}  align="center">
                    <Button variant="contained" color="secondary" onClick={this._backButtonPressed} id="back">
                        Back
                    </Button>
                </Grid>
            </Grid>
        );
    }

    _backButtonPressed() {
        const uname = localStorage.getItem('username');
        this.props.logInCallback((uname == null) ? "" : uname);
        this.props.history.push('/')
    }

    _handleUsernameTextFieldChange(e) {
        this.setState({
            username: e.target.value
        });
    }

    _handlePasswordTextFieldChange(e) {
        this.setState({
            password: e.target.value
        });
    }

    _loginButtonPressed() {

        if (!this.state.signUp) {
            const requestOptions = {
            method: "POST",
            headers: {"Content-Type": "application/json"},
            body: JSON.stringify({
                username: this.state.username,
                password: this.state.password,
            }),
            };
            fetch("/api/token-auth/", requestOptions)
            .then((response) => {
                if (response.ok) {
                    this.setState({
                        successMsg: "Signed in in successfully"
                    });
                    response.json().then((data) => {
                        localStorage.setItem("key", data.token)
                        localStorage.setItem("username", this.state.username)
                        this.props.logInCallback(this.state.username);
                        this.props.history.push('/')
                    })
                }
                else {
                    response.json().then((data) => {
                        this.setState({
                            errorMsg: "Invalid user or password"
                        });
                    })
                }
            });
        }
        else {
            const requestOptions = {
            method: "POST",
            headers: {"Content-Type": "application/json"},
            body: JSON.stringify({
                username: this.state.username,
                password: this.state.password,
            }),
            };
            fetch("/api/token-reg/", requestOptions)
            .then((response) => {
                if (response.ok) {
                    this.setState({
                        successMsg: "Signed up in successfully"
                    });
                    response.json().then((data) => {
                        localStorage.setItem("key", data.token)
                        localStorage.setItem("username", data.username)
                    })
                }
                else {
                    response.json().then((data) => {
                        this.setState({
                            errorMsg: "Invalid user or password"
                        });
                    })
                }
            });
        }
    }

    _optionButtonPressed() {
        this.setState({
            signUp: !this.state.signUp,
        })
    }
}