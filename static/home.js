function AbrirModal(id){
  if (id == 0){
    document.getElementsById("keyTitulo").innerHTML = "Agregar Paciente"
  } 
  else{
    document.getElementsById("keyTitulo").innerHTML = "Editar Paciente"
  }
}