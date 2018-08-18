import React from 'react'
import PropTypes from 'prop-types'

const FilaPropTypes = {
  apellido: PropTypes.string.isRequired,
  nombre: PropTypes.string.isRequired,
  dni: PropTypes.number,
  cantidad: PropTypes.number.isRequired,
  comentario: PropTypes.string,
  idColaboracion: PropTypes.number.isRequired,
  checkedBox: PropTypes.func,
}

const FilaColaboracion = ( props ) => {
  const { apellido, nombre, dni, cantidad, comentario, idColaboracion, checkedBox, entregado } = props
  return (
    <tr>
      <td>{apellido}</td>
      <td>{nombre}</td>
      <td>{dni ? dni : "-"}</td>
      <td>{cantidad}</td>
      <td>{comentario ? comentario : "-"}</td>
      <td><input 
            type="checkbox" 
            name={"entregado" + idColaboracion}              
            defaultChecked={entregado}
            onChange={() => checkedBox(idColaboracion)}/>
            </td>
    </tr>
  )
}
FilaColaboracion.propTypes = FilaPropTypes

export default FilaColaboracion;