import React, { Component } from 'react';
import { connect } from "react-redux";
import api from '../../../../api';

class ComentariosEvento extends Component {

  constructor(props) {
    super(props);
    const usuario = this.getUserId();
    this.state = {
      evento: this.props.evento,
      voluntario_id: usuario,
      participante: this.participante(this.props.evento, usuario),
      dioRetroalimentacion: this.dioRetroalimentacion(this.props.evento, usuario),
      comentario: '',
    }
    this.handleRetroalimentacion = this.handleRetroalimentacion.bind(this);
    this.handleInputChange = this.handleInputChange.bind(this);
    this.handleComentar = this.handleComentar.bind(this);
  }

  getOpcionComentar() {
    if (this.existeComentario(this.getUserId())) {
      return undefined;
    }
    return (
      <div className="row">
        <div className="col-md-10">
          <input type="text" name="comentario" className="form-control"
            placeholder="Escribe tu comentario..."
            value={this.state.comentario}
            onChange={this.handleInputChange}
          />
        </div>
        <div className="col-md-1">
          <button className="btn btn-primary" onClick={this.handleComentar}>Comentar</button>
        </div>
      </div>
    )
  }

  handleInputChange(event) {
    const target = event.target;
    const value = target.type === 'checkbox' ? target.checked : target.value;
    const name = target.name;
    this.setState({
        [name]: value
    });
  }

  handleComentar() {
    const comentario = {
      comentario: this.state.comentario,
      evento_id: this.state.evento.id,
      voluntario_id: this.state.voluntario_id
    }
    api.post('feedbacks/comentarios/', comentario)
      .then((res) => {
        this.props.update();
      })
      .catch((error) => {
        if (error.response){ console.log(error.response.status) }
        else { console.log('Error: ', error.message)}
      });
  }

  existeComentario(usuario) {
    return this.state.evento.comentarios.filter(c => c.voluntario.id === usuario).length > 0;
  }

  getOpiniones() {
    if (this.state.evento.comentarios.length > 0) {
      const opiniones = this.state.evento.comentarios.map((c) =>
        <div className="row">
            <div className="col-md-2">
            <b>{c.voluntario.nombre}</b>
            </div>
            <div className="col-md-2">
            <label>{c.comentario}</label>
            </div>
        </div>
      );
      return opiniones;
    }
  }

  dioRetroalimentacion(evento,usuario) {
    const necesidades = evento.necesidades;
    const voluntarios = evento.voluntarios;
    let filtroNecesidades;
    for (let i=0; i < necesidades.length; i++) {
      filtroNecesidades = necesidades[i].colaboraciones.filter(c => c.voluntario.id === usuario);
      return filtroNecesidades.length > 0 && filtroNecesidades[0].retroalimentacion;
    }
    let filtroVoluntarios;
    for (let i=0; i < voluntarios.length; i++) {
      filtroVoluntarios = voluntarios[i].participaciones.filter(c => c.voluntario.id === usuario);
      return filtroVoluntarios.length > 0 && filtroVoluntarios[0].retroalimentacion;
    }
    return false;
  }

  handleRetroalimentacion() {
    api.post('feedbacks/retroalimentacion/', { evento: this.state.evento.id })
      .then((res) => {
        this.props.update();
      })
      .catch((error) => {
        if (error.response){ console.log(error.response.status) }
        else { console.log('Error: ', error.message)}
      })
  }

  getOpcionRetroalimentacion() {
    if (!this.state.dioRetroalimentacion) {
      return (
        <div className="form-group">
          <button class="btn btn-primary" onClick={this.handleRetroalimentacion}>
            <i class="fa fa-thumbs-up"></i>Me gustó el evento
          </button>
          <label>Ayuda a la ONG en helpo si te gustó ser parte de esta actividad.</label>
        </div>
      )
    } else {
      return (
        <div className="form-group">
          <button class="btn btn-primary" disabled><i class="fa fa-thumbs-up"></i></button>
          <label className="label-group">Indicaste que te gustó el evento</label>
        </div>
      )
    }    
  }

  participante(evento, usuario) {
    const necesidades = evento.necesidades;
    const voluntarios = evento.voluntarios;
    for (let i=0; i < necesidades.length; i++) {
      if (necesidades[i].colaboraciones.filter(c => c.voluntario.id === usuario).length > 0){
        return true;
      }
    }
    for (let i=0; i < voluntarios.length; i++) {
      if (voluntarios[i].participaciones.filter(c => c.voluntario.id === usuario).length > 0){
        return true;
      }
    }
    return false;
  }

  getUserId() {
    return this.props.auth.user.id;
  }

  render() {
    const opiniones = this.getOpiniones();
    return (
      <div className="offset-md-1">
        <h2>Opiniones del evento</h2>
        {this.state.participante ?
          this.getOpcionRetroalimentacion()
        : undefined}
        {this.state.participante ?
          this.getOpcionComentar()
        : undefined}
        {opiniones}
      </div>
    )
  }
}

const mapStateToProps = state => {
  return {
    auth: state.auth,
  }
}
  
export default connect(mapStateToProps, undefined)(ComentariosEvento);