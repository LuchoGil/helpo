import React from 'react';
import { Card, CardHeader, CardBody, CardFooter } from 'reactstrap';
import { connect } from 'react-redux';
import api from '../../../api';
import ConsultarEventosList from './ConsultarEventosList';
import ConsultarEventosFilter from './ConsultarEventosFilter';
import ButtonsCompartirOrganizacion from '../../common/ButtonsCompartir/ButtonsCompartirOrganizacion';

class ConsultarEventosPage extends React.Component {

  constructor(props) {
    super(props);
    const urlParams = new URLSearchParams(this.props.location.search)
    const organizacion = urlParams.get('organizacion');
    this.state = {
      eventos: [],
      organizacion,
      ong: []
    }
    this.loadEventos = this.loadEventos.bind(this);
    this.loadONG = this.loadONG.bind(this);
  }

  getAuth() {
    return this.props.auth.isAuthenticated;
  }

  componentDidMount() {
    const ruta = this.state.organizacion ? '?organizacion=' + this.state.organizacion : '';
    this.loadEventos(ruta);
    if (this.state.organizacion) { this.loadONG() };
  }

  loadEventos(ruta) {
    api.get('/actividades/consulta_eventos/' + ruta)
      .then((res) => {
        this.setState({ eventos: res.data });
      })
      .catch((error) => {
        if (error.response) { console.log(error.response.status) }
        else { console.log('Error: ', error.message) }
      })
  }

  loadONG() {
    api.get(`/perfiles/perfil_organizacion/${this.state.organizacion}/`)
      .then((res) => {
        this.setState({ ong: res.data.usuario });
      })
      .catch((error) => {
        this.setState({ ong: undefined });
        if (error.response) { console.log(error.response.status) }
        else { console.log('Error: ', error.message) }
      })
  }

  renderEventos() {
    const eventos = this.state.eventos;
    if (eventos.length === 0) {
      return (
        <CardBody>
          <ConsultarEventosFilter updatePath={this.loadEventos} organizacion={this.state.organizacion} />
          <br />
          <label>&emsp;Todav&iacute;a no hay eventos registrados</label>
        </CardBody>
      )
    }
    else {
      return (
        <CardBody>
          <ConsultarEventosFilter updatePath={this.loadEventos} />
          <br />
          <ConsultarEventosList eventos={eventos} auth={this.getAuth()} />
        </CardBody>
      )
    }
  }

  renderCompartir() {
    const organizacion = this.state.organizacion;
    if (organizacion) {
      const ong = this.state.ong;
      if (ong) {
        return (
          <CardFooter>
            <div className="row">
              <div className="form-group">
                <b name="compartir" className="float-left">Compartir</b>
              </div>
              <div className="form-group">
                <div className="float-left offset-md-3">
                  <ButtonsCompartirOrganizacion ong={ong} />
                </div>
              </div>
            </div>
          </CardFooter>
        )
      }
    }
    else {
      return undefined;
    }
  }

  render() {
    return (
      <div className="animated fadeIn">
        <Card>
          <CardHeader>
            <i className="fa fa-align-justify"></i> Eventos
          </CardHeader>
          {this.renderEventos()}
          {this.renderCompartir()}
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
