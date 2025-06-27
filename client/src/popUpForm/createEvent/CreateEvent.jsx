import React, { useState } from 'react';
import { Modal, Button, Form, Col } from 'react-bootstrap';
import 'bootstrap/dist/css/bootstrap.min.css';
import './createEvent.css';

const CreateEvent = ({ show, onClose, onSave, onDelete, isEditMode = false }) => {
  const [eventData, setEventData] = useState({
    title: '',
    description: '',
    interests: [],
    location: '',
    date: '',
    image: null,
    imagePreview: '',
  });

  const interestsOptions = [
    'Спорт',
    'Искусство',
    'Музыка',
    'Кино',
    'Наука',
    'Технологии',
    'Путешествия',
    'Еда',
  ];

  const handleInputChange = (e) => {
    const { name, value } = e.target;
    setEventData({ ...eventData, [name]: value });
  };

  const handleInterestChange = (e) => {
    const selectedOptions = Array.from(e.target.selectedOptions, (option) => option.value);
    setEventData({ ...eventData, interests: selectedOptions });
  };

  const handleImageChange = (e) => {
    const file = e.target.files[0];
    if (file) {
      // Проверка размера файла
      if (file.size > 5 * 1024 * 1024) {
        alert('Файл слишком большой. Максимальный размер: 5MB');
        return;
      }
  
      const reader = new FileReader();
      reader.onloadend = () => {
        setEventData({
          ...eventData,
          image: file, // Сохраняем объект File для FormData
          imagePreview: reader.result
        });
      };
      reader.readAsDataURL(file);
    }
  };

  // В компоненте CreateEvent.jsx
const handleSubmit = (e) => {
  e.preventDefault();
  
  // Валидация данных
  if (eventData.interests.length === 0) {
    alert('Пожалуйста, выберите хотя бы один интерес');
    return;
  }

  // Преобразование данных перед отправкой
  const apiData = {
    title: eventData.title,
    description: eventData.description,
    interests: eventData.interests,
    location: eventData.location,
    start_time: eventData.date,
    image: eventData.image
  };

  onSave(apiData); // Передача данных в родительский компонент
  onClose(); // Закрытие модалки
};

  return (
    <Modal show={show} onHide={onClose} size="lg" centered>
      <Modal.Header closeButton>
        <Modal.Title>
          {isEditMode ? 'Редактировать мероприятие' : 'Создать мероприятие'}
        </Modal.Title>
      </Modal.Header>

      <Form onSubmit={handleSubmit}>
        <Modal.Body>
          {/* Блок загрузки изображения */}
          <Form.Group className="mb-4 text-center">
            {eventData.imagePreview ? (
              <div className="position-relative">
                <img
                  src={eventData.imagePreview}
                  alt="Предпросмотр"
                  className="img-fluid rounded mb-2"
                  style={{ maxHeight: '200px' }}
                />
                <Form.Label className="btn btn-outline-primary mt-2">
                  Изменить изображение
                  <Form.Control
                    type="file"
                    accept="image/*"
                    onChange={handleImageChange}
                    className="d-none"
                  />
                </Form.Label>
              </div>
            ) : (
              <Form.Label className="d-block border rounded p-4" style={{ cursor: 'pointer' }}>
                <div className="text-center">
                  <div style={{ fontSize: '2rem' }}>+</div>
                  <div className="fw-bold">Добавить изображение</div>
                  <div className="text-muted">JPG, PNG до 5MB</div>
                  <Form.Control
                    type="file"
                    accept="image/*"
                    onChange={handleImageChange}
                    className="d-none"
                  />
                </div>
              </Form.Label>
            )}
          </Form.Group>

          <Form.Group className="mb-3">
            <Form.Label>Название мероприятия</Form.Label>
            <Form.Control
              type="text"
              name="title"
              value={eventData.title}
              onChange={handleInputChange}
              required
            />
          </Form.Group>

          <Form.Group className="mb-3">
            <Form.Label>Описание</Form.Label>
            <Form.Control
              as="textarea"
              rows={3}
              name="description"
              value={eventData.description}
              onChange={handleInputChange}
              required
            />
          </Form.Group>

          <Form.Group className="mb-3">
            <Form.Label>Интересы</Form.Label>
            <Form.Select
              multiple
              name="interests"
              value={eventData.interests}
              onChange={handleInterestChange}
              required
              className={eventData.interests.length === 0 ? 'is-invalid' : ''}>
              {interestsOptions.map((interest) => (
                <option key={interest} value={interest}>
                  {interest}
                </option>
              ))}
            </Form.Select>
            <Form.Text className="text-muted">
              Удерживайте Ctrl для выбора нескольких вариантов
            </Form.Text>
            {eventData.interests.length === 0 && (
              <div className="invalid-feedback">Пожалуйста, выберите хотя бы один интерес</div>
            )}
          </Form.Group>

          <Form.Group className="mb-3">
            <Form.Label>Место проведения</Form.Label>
            <Form.Control
              type="text"
              name="location"
              value={eventData.location}
              onChange={handleInputChange}
              required
            />
          </Form.Group>

          <Form.Group className="mb-3">
            <Form.Label>Дата и время проведения</Form.Label>
            <Form.Control
              type="datetime-local"
              name="date"
              value={eventData.date}
              onChange={handleInputChange}
              required
            />
          </Form.Group>
        </Modal.Body>

        <Modal.Footer>
          {isEditMode && (
            <Button variant="danger" onClick={onDelete}>
              Удалить
            </Button>
          )}
          <Button variant="secondary" onClick={onClose}>
            Закрыть
          </Button>
          <Button variant="primary" type="submit">
            {isEditMode ? 'Обновить' : 'Создать'}
          </Button>
        </Modal.Footer>
      </Form>
    </Modal>
  );
};

export default CreateEvent;
