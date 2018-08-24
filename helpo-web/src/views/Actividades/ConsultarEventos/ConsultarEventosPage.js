import React from 'react';  
import { Card, CardHeader, CardBody } from 'reactstrap';
import {connect} from 'react-redux';
import api from '../../../api';
import ConsultarEventosList from './ConsultarEventosList';
import ConsultarEventosFilter from './ConsultarEventosFilter';

class ConsultarEventosPage extends React.Component {

  constructor(props) {
    super(props);
    this.state = {
      eventos: [],
    }
    this.loadEventos = this.loadEventos.bind(this);
  }

  getAuth() {
    return this.props.auth.isAuthenticated;
  }

  componentDidMount() {
    this.loadEventos('');
  }

  loadEventos(ruta) {
    api.get('/actividades/consulta_eventos/' + ruta)
      .then((res) => {
        this.setState({ eventos: res.data });
      })
      .catch((error) => {
        if (error.response){ console.log(error.response.status) }
        else { console.log('Error: ', error.message)}
      })
  }

  renderEventos(){
    const eventos = this.state.eventos;
    if(eventos.length === 0){
      return(
        <div className="row">
          <div className="form-group col-md-6 col-md-offset-3">
            <label>&emsp;Todav&iacute;a no hay eventos registrados</label>
          </div>
        </div>
      )
    }
    else{
      return(
        <CardBody>
          <ConsultarEventosFilter updatePath={this.loadEventos} />
          <br />
          <ConsultarEventosList eventos={eventos} auth={this.getAuth()} />
        </CardBody>
      )
    }
  }

  render() {
    return (
      <div className="animated fadeIn">
        <Card>
          <CardHeader>
            <i className="fa fa-align-justify"></i> Consultar eventos
          </CardHeader>
          {this.renderEventos()}
        </Card>
      </div>
    );
  }
}

function mapStateToProps(state, ownProps) {
  return {
    auth: state.auth, 
  }
}
export default connect(mapStateToProps, undefined)(ConsultarEventosPage);
