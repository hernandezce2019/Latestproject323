class user {
    constructor (
        nombre,
        apellido,
        cedula,
        correo,
        direccion,
        fecha,

     )
      {
        this.nombre=nombre;
        this.apellido=apellido;
        this.cedula=cedula;
        this.correo=correo;
        this.direccion=direccion; 
        this.fecha=fecha;
      };
    
      fecha() {
        let now = new Date();
        let acquired = new Date(this.dateAcquired);
        let elapsed = now - acquired; // elapsed time in milliseconds
        let daysSinceAcquired = Math.floor(elapsed / (1000 * 3600 * 24));
        return daysSinceAcquired;
    }
}

export default user;

