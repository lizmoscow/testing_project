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
            username: this.props.username,
            error: "",
        };
        this._logInButton = this._logInButton.bind(this);
        this._logOut = this._logOut.bind(this);
        this.getUsername = this.getUsername.bind(this);
        this._joinButton = this._joinButton.bind(this);
        this._createButton = this._createButton.bind(this);
    }

    async componentDidMount() {

        const uname = localStorage.getItem('username');
        console.log("username is " + uname)
        this.setState({
            username: (uname == null) ? "" : uname,
        });
    }

    getUsername(username) {
        this.setState({
            username: username,
        });
    }

    _logOut() {
        localStorage.removeItem('key')
        localStorage.removeItem('username')
        this.setState({
            username: "",
        });
    }

    _logInButton() {
        if (this.state.username == "") {
            return (
                <Button color="primary" to='/login' component={Link} id="login-button">
                    Log in
                </Button>
            );
        }
        return (
            <Button color="primary" to='/login' onClick={this._logOut} id="login-button">
                    Log out
            </Button>
        );
    }


    _joinButton() {
        if (localStorage.getItem('key') != null) {
            return(
                <Button color="primary" to='/join' component={Link} id="join-group">
                                Join a Room
                </Button>
            )
        }
        return("");
    }


    _createButton() {
        if (localStorage.getItem('key') != null) {
            return(
                <Button color="secondary" to='/create' component={Link} id="create-group">
                    Create a Room
                </Button>
            )
        }
        return("");
    }


    _renderHomePage() {
        return (
            <Grid container spacing={3}>
                <Grid item xs={12} align="center">
                    <Typography variant="h3" compact="h3" id="page-title">
                        {"House Party" + ((this.state.username != "") ? " with " +
                            this.state.username : "")}
                    </Typography>
                </Grid>
                <Grid item xs={12} align="center">
                    <ButtonGroup disableElevation
                                 variant="contained"
                                 color="primary">
                        {this._joinButton()}
                        {this._createButton()}
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
                <Route path='/room/:roomCode' component={Room} />
            </Switch>
        </Router>;
    }
}