// import React from 'react';
// import Button from 'react-bootstrap/Button';
// import Modal from 'react-bootstrap/Modal';
// import '../../element/card/cardStaff/cardStaff.css'

// function CheckedStaff({ show, event, handleClose }) {
//   function formatTime(dateString) {
//     const date = new Date(dateString);
//     const hours = date.getHours().toString().padStart(2, '0');
//     const minutes = date.getMinutes().toString().padStart(2, '0');
//     const day = date.getDate().toString().padStart(2, '0');
//     const month = (date.getMonth() + 1).toString().padStart(2, '0');
//     const year = date.getFullYear();

//     return `${hours}:${minutes} ${day}.${month}.${year}`;
//   }

//   return (
//     <Modal
//       show={show}
//       onHide={handleClose}
//       backdrop="static"
//       keyboard={false}
//       dialogClassName="custom-modal">
     

//       <Modal.Body>
//       <div className="cardStaff__wrapper">
//             <a href="/checkedStaff" className="cardStaff__items">
//                 <img src={require('../../image/face.jpg')} alt="" />
//                 <div className="cardStaff__content">
//                     <h3 className='cardStaff__content-name'>{event.username}</h3>
//                     <p className='cardStaff__content-all cardStaff__content-position'>Должность: {event.position}</p>
//                     <p className='cardStaff__content-all cardStaff__content-position'>Должность: {event.position}</p>
//                     <p className='cardStaff__content-all cardStaff__content-position'>Должность: {event.position}</p>
//                     <p className='cardStaff__content-all cardStaff__content-position'>Должность: {event.position}</p>
//                     <p className='cardStaff__content-all cardStaff__content-position'>Должность: {event.position}</p>
//                     <p className='cardStaff__content-all cardStaff__content-position'>Должность: {event.position}</p>
//                     <p className='cardStaff__content-all cardStaff__content-position'>Должность: {event.position}</p>
//                     <p className='cardStaff__content-all cardStaff__content-departament'>Отдел: {event.department}</p>
//                     <p className='cardStaff__content-all cardStaff__content-tel'>Телефон: {event.telephone}</p>
//                     <p className='cardStaff__content-all jcardStaff__content-email'>Email: {event.email}</p>
//                 </div>
//                 <ul className="cardStaff__inter">
//                     <li >{event.interests}</li>
//                 </ul>
//             </a>
//         </div>
//       </Modal.Body>
//       <Modal.Footer
//         style={{
//           display: 'flex',
//           flexDirection: 'row',
//           justifyContent: 'space-between',
//           alignItems: 'center',
//         }}>
//         <Button variant="" style={{ borderRadius: '15px' }} onClick={handleClose}>
//           Закрыть
//         </Button>
//         <Button variant="primary" style={{ borderRadius: '15px' }}>
//           Записаться
//         </Button>
//       </Modal.Footer>
//     </Modal>
//   );
// }

// export {CheckedStaff};
