import Button from 'react-bootstrap/Button';
import Col from 'react-bootstrap/Col';
import Form from 'react-bootstrap/Form';
import Row from 'react-bootstrap/Row';

function Registration() {
  return (
    <Form>
      <Row className="mb-3">
        <Form.Group as={Col} controlId="formGridEmail">
          <Form.Control type="email" placeholder="Email/Телефон" />
        </Form.Group>

        <Form.Group as={Col} controlId="formGridPassword">

          <Form.Control type="password" placeholder="Пароль" />
        </Form.Group>
      </Row>

      
      

      
      <Row className="mb-3">
        <Form.Group as={Col} controlId="formGridState">
          <Form.Label>Выберите должность</Form.Label>
          <Form.Select defaultValue="Не выбрано">
            <option>Не выбрано</option>
            <option>1</option>
            <option>2</option>
            <option>3</option>
            <option>4</option>
            <option>5</option>
            <option>6</option>
            <option>7</option>
            <option>...</option>
          </Form.Select>
        </Form.Group>
      </Row>
      
      <Row className="mb-3">
        <Form.Group as={Col} controlId="formGridState">
          <Form.Label>Выберите отдел</Form.Label>
          <Form.Select defaultValue="Не выбрано">
            <option>Не выбрано</option>
            <option>1</option>
            <option>2</option>
            <option>3</option>
            <option>4</option>
            <option>5</option>
            <option>6</option>
            <option>7</option>
            <option>...</option>
          </Form.Select>
        </Form.Group>
      </Row>

      <Form.Group className="mb-3" id="formGridCheckbox">
        <Form.Check type="checkbox" label="Я согласен с политикой конфиденциальности" />
      </Form.Group>

      <Button variant="primary" type="submit">
        Зарегистрироваться
      </Button>
    </Form>
  );
}

export {Registration};