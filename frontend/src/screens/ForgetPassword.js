import React, { useState } from "react";

/* REACT ROUTER */
import { Link } from "react-router-dom";

/* REACT BOOTSTRAP */
import { Button, Form } from "react-bootstrap";

/* COMPONENTS */
import Message from "../components/Message";
import Loader from "../components/Loader";
import FormContainer from "../components/FormContainer";

/* REACT - REDUX */
import { useDispatch, useSelector } from "react-redux";

/* ACTION CREATORS */
import { reset_password } from "../actions/userActions";

function ForgetPassword({ location }) {
  /* STATE */
  const [formData, setFormData] = useState({ email: "" });
  const { email } = formData;
  const [requestSend, setRequestSend] = useState(false);
  const dispatch = useDispatch();
  const userLogin = useSelector((state) => state.userLogin);

  // const onChange = (e) =>
  //   setFormData({ ...formData, [e.target.name]: e.target.value });
  const { loading, error } = userLogin;

  /* SETTING UP REDIRECT */
  // const redirect = location.search ? location.search.split("=")[1] : "/";

  const submitHandler = (e) => {
    e.preventDefault();
    
    // reset_password(formData);
    setRequestSend(true);

    /* FIRING OFF THE ACTION CREATORS USING DISPATCH FOR LOGIN */
    dispatch(reset_password(formData));
  };
  return (
    <FormContainer>
      <h1>Password Reset</h1>

      {error && <Message variant="danger">{error}</Message>}
      {loading && <Loader />}

      <Form
        onSubmit={submitHandler}
        method="POST"
        encType="multipart/form-data"
      >
        <Form.Group controlId="email">
          <Form.Label>Email Address</Form.Label>
          <Form.Control
            type="email"
            placeholder="Enter Email"
            name="email"
            value={email}
            onChange={(e) => setFormData(e.target.value)}
          />
        </Form.Group>
        {/* to={redirect && `/password_reset?redirect=${redirect}` } */}
        <Link>
          <Button type="submit" variant="primary" className="mt-3">
            Search
          </Button>
        </Link>

        <Link to="/login">
          <Button variant="outline-primary" className="mt-3">
            Cancel
          </Button>
        </Link>
      </Form>
    </FormContainer>
  );
}
export default ForgetPassword;
