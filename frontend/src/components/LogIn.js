import React, {Component} from "react";
import {TextField, Button, Grid, Typography, Collapse} from "@material-ui/core";
import {Link} from "react-router-dom";
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
    }

    render() {
        return (
            <Grid container spacing={1}>
                <Grid item xs={12} align="center">
                <Collapse in={this.state.errorMsg || this.state.successMsg}>
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
                    <Typography variant="h4" component="h4">
                        {(!this.state.signUp) ? "Sign In" : "Sign Up"}
                    </Typography>
                </Grid>
                <Grid item xs={12} align="center">
                    <TextField
                        error={this.state.error}
                        label="Username"
                        placeholder="Enter a username"
                        value={this.state.username}
                        variant="outlined"
                        onChange={this._handleUsernameTextFieldChange}
                    />
                </Grid>
                <Grid item xs={12} align="center">
                    <TextField
                        error={this.state.error}
                        label="Password"
                        placeholder="Enter a password"
                        value={this.state.password}
                        variant="outlined"
                        type="password"
                        onChange={this._handlePasswordTextFieldChange}
                    />
                </Grid>
                <Grid item xs={12}  align="center">
                    <Button variant="contained" color="primary" onClick={this._loginButtonPressed}>
                        {(!this.state.signUp) ? "Sign In" : "Sign Up"}
                    </Button>
                </Grid>
                <Grid item xs={12}  align="center">
                    <Button variant="contained" color="primary" onClick={this._optionButtonPressed}>
                        {(!this.state.signUp) ? "Don't Have an Account Yet?" : "Already Have an Account?"}
                    </Button>
                </Grid>
                <Grid item xs={12}  align="center">
                    <Button variant="contained" color="secondary" to="/" component={Link}>
                        Back
                    </Button>
                </Grid>
            </Grid>
        );
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
            fetch("/api/dj-rest-auth/login/", requestOptions)
            .then((response) => {
                if (response.ok) {
                    this.setState({
                        successMsg: "Signed in in successfully"
                    });
                }
                else {
                    response.json().then((data) => {
                        if (data.password)
                        this.setState({
                            errorMsg: data.password,
                        });
                        if (data.username)
                        this.setState({
                            errorMsg: data.username,
                        });
                        if (data.non_field_errors)
                        this.setState({
                            errorMsg: data.non_field_errors,
                        });
                    })
                }
                return response.json()
            }).then((data) => {
                localStorage.setItem("key", data.key)
        }).then((data) => {
            this.props.logInCallback();
            this.props.history.push('/')});
        }
        else {
            const requestOptions = {
            method: "POST",
            headers: {"Content-Type": "application/json"},
            body: JSON.stringify({
                username: this.state.username,
                password1: this.state.password,
                password2: this.state.password,
            }),
        };
            fetch("/api/dj-rest-auth/registration/", requestOptions)
            .then((response) => {
                if (response.ok) {
                    this.setState({
                        successMsg: "Signed up in successfully"
                    });
                }
                else {
                    response.json().then((data) => {
                        if (data.password1)
                        this.setState({
                            errorMsg: data.password1,
                        });
                        if (data.username)
                        this.setState({
                            errorMsg: data.username,
                        });
                        if (data.non_field_errors)
                        this.setState({
                            errorMsg: data.non_field_errors,
                        });
                    })
                }
            }).then((response) => {
                if (response.ok) {
                    localStorage.setItem("key", response.json().key)
                }
        }).then((data) => {
            this.props.logInCallback();
            this.props.history.push('/')});
        }
    }

    _optionButtonPressed() {
        this.setState({
            signUp: !this.state.signUp,
        })
    }
}