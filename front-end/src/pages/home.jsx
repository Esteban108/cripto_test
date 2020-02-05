import React, {Component} from 'react';
import Sidebar from './components/sidebar'
import Introduction from './components/introduction'
import About from './components/about'
import Loading from './components/loading'
import BigMessage from './components/succes'

class Home extends Component {
    render() {
        return (
            <div id="">
                <div id="container-wrap">
                    <Sidebar home={true}   getAuth={this.props.getAuth} setAuth={this.props.setAuth} toggleLoading={this.props.toggleLoading}
                             toggleBigMessage={this.props.toggleBigMessage}/>
                    <div id="colorlib-main">
                        <Introduction/>
                        <About/>
                    </div>
                </div>
            </div>
        );
    }
}
export default Home;