import React, {Component} from "react";
import RoomJoinPage from "./RoomJoinPage";
import CreateRoomPage from "./CreateRoomPage";
import Room from "./Room";
import LogIn from "./LogIn";
import {BrowserRouter as Router, Switch, Route, Link, Redirect} from "react-router-dom";
import {Grid, Button, ButtonGroup, Typography} from "@material-ui/core";

export  default class HomePage extends Component {
    static defaultProps = {
        username: "",
    };
    constructor(props) {
        super(props);
        this.state = {
            roomCode: null,
            username: this.props.username,
            error: "",
        };
        this.clearRoomCode = this.clearRoomCode.bind(this);
        this._logInButton = this._logInButton.bind(this);
        this._logOut = this._logOut.bind(this);
        this.getUsername = this.getUsername.bind(this);
    }

    async componentDidMount() {
         const requestOptions = {
            method: "GET",
            credentials: 'omit',
        };
        fetch('/api/user_in_room', requestOptions)
            .then((response) => response.json())
            .then((data) => {this.setState({
                roomCode: data.code,
            });
            });
        this.getUsername();
    }

    getUsername() {
            fetch("/api/dj-rest-auth/user/")
            .then((response) => response.json()
            )
            .then((data) => {
                if (data.username) {
                this.setState({
                    username: data.username,
                });
            }
        });


    }

    clearRoomCode() {
        this.setState({
            roomCode: null,
        });
    }

    _logOut() {
        const requestOptions = {
            method: "GET",
            headers: {"Content-Type": "application/json",
                'Accept': 'application/json',}
        };
        fetch("/api/dj-rest-auth/logout/", requestOptions)
            .then((response) => {
            if (response.ok) {
                localStorage.setItem("key", "");
                this.setState({
                    username: "",
                });
            }
            else {
                this.setState({
                    error: "Can not log out"
                });
            }
        }).catch((error) => { console.log(code); });
    }

    _logInButton() {
        if (this.state.username == "") {
            return (
                <Button color="primary" to='/login' component={Link}>
                    Log in
                </Button>
            );
        }
        return (
            <Button color="primary" to='/login' onClick={this._logOut}>
                    Log out
            </Button>
        );
    }

    _renderHomePage() {
        return (
            <Grid container spacing={3}>
                <Grid item xs={12} align="center">
                    <Typography variant="h3" compact="h3">
                        {"House Party" + ((this.state.username != "") ? " with " +
                            this.state.username : "")}
                    </Typography>
                </Grid>
                <Grid item xs={12} align="center">
                    <ButtonGroup disableElevation
                                 variant="contained"
                                 color="primary">
                        <Button color="primary" to='/join' component={Link}>
                            Join a Room
                        </Button>
                        <Button color="secondary" to='/create' component={Link}>
                            Create a Room
                        </Button>
                        {this._logInButton()}
                    </ButtonGroup>
                </Grid>
            </Grid>
        );
    }

    render() {
        return <Router>
            <Switch>
                <Route exact path='/' render={() => {
                    return this.state.roomCode ? (<Redirect to={`/room/${this.state.roomCode}`}/>) : this._renderHomePage()
                }}/>
                <Route path='/join' component={RoomJoinPage} />
                <Route path='/create' component={CreateRoomPage} />
                <Route path='/login' render={(props) => {
                           return <LogIn {...props} logInCallback={this.getUsername} />
                       }} />
                <Route path='/room/:roomCode'
                       render={(props) => {
                           return <Room {...props} leaveRoomCallback={this.clearRoomCode} />
                       }}/>
            </Switch>
        </Router>;
    }
}