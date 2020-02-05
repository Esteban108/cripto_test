import React, {Component} from 'react'
import Spinner from "react-bootstrap/Spinner";

class Loading extends Component {

    render() {
        return (
            <>
                <div id="loading" className={"overlay"} hidden={!this.props.loading}>
                    <div style={{display: 'flex', justifyContent: 'center', alignItems: 'center', height: '100vh'}}>

                        <Spinner style={{width: "10%", height: "20%"}} className="popup" animation="border"
                                 variant="warning"/>
                    </div>
                </div>
            </>
        );
    }
}

export default Loading;