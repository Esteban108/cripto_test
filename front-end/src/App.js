import React, {Component} from 'react';
import './App.css';
import 'bootstrap/dist/css/bootstrap.min.css';
import Home from "./pages/home";
import Private from "./pages/private";
import {BrowserRouter as Router, Route, Switch} from "react-router-dom";
import Loading from "./pages/components/loading";
import BigMessage from "./pages/components/succes";

class App extends Component {
    constructor(props) {
        super(props);
        this.state = {
            loading: false,
            big_msg: false,
            big_msg_text: "",
            big_msg_icon: "",
            big_msg_small_text: "",
            auth: ""
        };
    }

    toggleLoading = () => {
        this.setState({loading: !this.state.loading})
    };
    setAuth = (auth) => {
        this.setState({auth: window.btoa(auth)});
    };
    getAuth = () => {
        return window.atob(this.state.auth)
    };
    toggleBigMessage = (text = "", icon = "", small_text = "") => {
        this.setState({
            big_msg: !this.state.big_msg,
            big_msg_text: text, big_msg_icon: icon,
            big_msg_small_text: small_text
        });
    };
    componentDidUpdate = () => {
        if (this.state.big_msg) {
            setTimeout(() => this.toggleBigMessage(), 3000);
        }
    };

    render() {
        return (
            <Router>
                <Switch>
                    <Route exact path="/">
                        <Loading loading={this.state.loading}/>
                        <BigMessage small_text={this.state.big_msg_small_text}
                                    icon={this.state.big_msg_icon}
                                    text={this.state.big_msg_text}
                                    show={this.state.big_msg}/>
                        <Home
                            setAuth={this.setAuth}
                            getAuth={this.getAuth}
                            toggleBigMessage={this.toggleBigMessage}
                            toggleLoading={this.toggleLoading}
                        />
                    </Route>
                    <Route exact path="/private">
                        <Private
                            getAuth={this.getAuth}
                            toggleBigMessage={this.toggleBigMessage}
                            toggleLoading={this.toggleLoading}
                        />
                    </Route>
                </Switch>
            </Router>
        );
    }
}

export default App;