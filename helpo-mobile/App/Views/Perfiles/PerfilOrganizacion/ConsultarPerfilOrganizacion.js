import React, { Component } from 'react';
import { connect } from 'react-redux';
import {
  Container,
  Header,
  Title,
  Content,
  Button,
  Label,
  ListItem,
  Body,
  Left,
  Right,
  Icon,
  Thumbnail,
  Text,
  Separator
} from 'native-base';
import styles from './styles';


class ConsultarPerfilOrganizacion extends Component {
  constructor(props) {
    super(props);
    this.renderDescripcion = this.renderDescripcion.bind(this);
    this.renderRubro = this.renderRubro.bind(this);
    this.renderTelefono = this.renderTelefono.bind(this);
    this.renderDescripcion = this.renderDescripcion.bind(this);
    this.renderCuit = this.renderCuit.bind(this);
  }

  renderRubro() {
    if (this.props.data.rubro == null) {
      return <Text style={styles.textMuted}> No hay valor ingresado</Text>
    }
    return <Text> {this.props.data.rubro.nombre}</Text>
  }

  renderTelefono() {
    //Si uso == va a dar True para null y undefined
    if (this.props.data.telefono == null) {
      return <Text style={styles.textMuted}> No hay valor ingresado</Text>
    }
    return <Text> {this.props.data.telefono}</Text>
  }

  renderCuit() {
    if (this.props.data.cuit == null) {
      return <Text style={styles.textMuted}> No hay valor ingresado</Text>
    }
    return <Text> {this.props.data.cuit}</Text>
  }

  renderDescripcion() {
    if (this.props.data.descripcion == null) {
      return <Text style={styles.textMuted}> No hay valor ingresado</Text>
    }
    return <Text> {this.props.data.descripcion}</Text>
  }

  getBotonOrganizacion() {
    if (this.props.data.usuario.id === this.props.auth.user.id) {
      return (
        <Button transparent onPress={this.props.switchToModificar}>
          <Text>Modificar</Text>
        </Button>
      );
    } else if (this.props.data.usuario.user_type === 1) {
      return (
        <Button transparent onPress={this.props.switchToEventosOrg}>
          <Text>Ver eventos</Text>
        </Button>
      );
    }
  }

  render() {
    if (this.props.data.avatar) {
      return (
        <Container style={styles.container}>
          <Header>
            <Left>
              <Button transparent onPress={this.props.goBack}>
                <Icon name="arrow-back" />
              </Button>
            </Left>
            <Body>
              <Title>Perfil</Title>
            </Body>
            <Right>
              {this.getBotonOrganizacion()}
            </Right>
          </Header>
          <Content>
            <Thumbnail large center source={{ uri: this.props.data.avatar.url }} />
            <ListItem itemDivider>
              <Label style={styles.label}>Nombre</Label>
            </ListItem>
            <ListItem>
              <Text>{this.props.nombre}</Text>
            </ListItem>

            <ListItem itemDivider>
              <Label style={styles.label}>Mail</Label>
            </ListItem>
            <ListItem>
              <Text>{this.props.email}</Text>
            </ListItem>

            <ListItem itemDivider>
              <Label style={styles.label}>Teléfono</Label>
            </ListItem>
            <ListItem>
              {this.renderTelefono()}
            </ListItem>

            <ListItem itemDivider>
              <Label style={styles.label}>CUIT</Label>
            </ListItem>
            <ListItem>
              {this.renderCuit()}
            </ListItem>

            <ListItem itemDivider>
              <Label style={styles.label}>Rubro</Label>
            </ListItem>
            <ListItem>
              {this.renderRubro()}
            </ListItem>

            <ListItem itemDivider>
              <Label style={styles.label}>Descripción</Label>
            </ListItem>
            <ListItem>
              {this.renderDescripcion()}
            </ListItem>

          </Content>
        </Container>
      );
    } else {
      return <Text></Text>
    }

  }
}

const mapStateToProps = state => ({
  auth: state.auth,
});

export default connect(mapStateToProps, undefined)(ConsultarPerfilOrganizacion);