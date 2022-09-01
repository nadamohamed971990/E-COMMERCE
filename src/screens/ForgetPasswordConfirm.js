import React, { useState } from "react";

/* REACT ROUTER */
// import { Link } from "react-router-dom";

/* REACT BOOTSTRAP */
import { Button, Form } from "react-bootstrap";

/* COMPONENTS */
import Message from "../components/Message";
import Loader from "../components/Loader";
import FormContainer from "../components/FormContainer";

/* REACT - REDUX */
import { useDispatch,useSelector } from "react-redux";

/* ACTION CREATORS */
// import { reset_password_confirm } from "../actions/userActions";

function ForgetPasswordConfirm({ match, reset_password_confirm }) {
  /* STATE */
  const [formData, setFormData] = useState({
    new_password: "",
    re_new_password: "",
  });
  const { new_password, re_new_password } = formData;
  const [requestSend, setRequestSend] = useState(false);

  const dispatch = useDispatch();
  const userLogin = useSelector((state) => state.userLogin);

  const onChange = (e) => 
    setFormData({ ...formData, [e.target.name]: e.target.value });

  const { loading, error } = userLogin;

  const submitHandler = (e) => {
    e.preventDefault();

    const uid = match.params.uid;
    const token = match.params.token;

    reset_password_confirm(uid, token, new_password, re_new_password);
    setRequestSend(true);

    /* FIRING OFF THE ACTION CREATORS USING DISPATCH FOR LOGIN */
    dispatch(reset_password_confirm(formData));
  };

  return (
    <FormContainer>
      <h1>Password Reset</h1>

      {error && <Message variant="danger">{error}</Message>}
      {loading && <Loader />}

      <Form onSubmit={submitHandler}>
        <Form.Group controlId="password">
          <Form.Label>New Password</Form.Label>
          <Form.Control
            type="password"
            placeholder="Enter New Password"
            name="new_password"
            value={new_password}
            onChange={(e) => setFormData(e.target.value)}
          />
        </Form.Group>

        <Form.Group controlId="password">
          <Form.Label>Confirm New Password</Form.Label>
          <Form.Control
            type="password"
            name="re_new_password"
            value={re_new_password}
            placeholder="Confirm New Password"
            onChange={(e) => setFormData(e.target.value)}
          />
        </Form.Group>

        <Button type="submit" variant="primary" className="mt-3">
          Reset Password
        </Button>
      </Form>
    </FormContainer>
  );
}
export default ForgetPasswordConfirm;
