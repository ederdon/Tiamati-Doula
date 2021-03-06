import React, { useContext, useState, useEffect } from "react";
import { Context } from "../store/appContext";
import { Calendar } from "../component/calendar";
import { useHistory } from "react-router-dom";
import "../../styles/appointment.css";

export const Appointment = () => {
  let history = useHistory();
  const { store, actions } = useContext(Context);
  const [showAppointment, setShowAppointment] = useState(false);
  const [hourSelected, setHourSelected] = useState();
  const [serviceID, setServiceID] = useState();
  const [serviceName, setServiceName] = useState();
  const [dataSaved, setDataSaved] = useState(false);
  const [showCalendar, setShowCalendar] = useState(false);
  const [showService, setShowService] = useState(true);
  const [showTitle, setShowTitle] = useState(true);
  const [dateTime, setDateTime] = useState({
    service: "",
    date: "",
    time: "",
  });

  useEffect(() => {
    setDateTime({
      ...dateTime,
      service: serviceID,
      date: store.dateSelected,
      time: hourSelected,
    });
  }, [hourSelected]);

  useEffect(() => {
    actions.verify();
  }, []);

  const saveUserAppointment = async () => {
    const response = await fetch(store.url + "/appointment", {
      method: "POST",
      body: JSON.stringify(dateTime),
      headers: {
        "Content-Type": "application/json",
        authorization: "Bearer " + localStorage.getItem("token"),
      },
    });
    const data = await response.json();
  };

  return (
    <div className="appointment container">
      {showCalendar == true ? <Calendar className="mx-5" /> : null}
      <div className="make-appointment">
        <h2>{showTitle == true ? "RESERVA TU CITA" : null}</h2>
        <div id="datetime" className="">
          {showService == true ? (
            <div>
              <div className="datetime-header py-1">
                <h6 className="pt-2">SERVICIO</h6>
              </div>
              <div className="datetime-body">
                <p className="mt-2">¿Para qué servicio quieres la cita?</p>
                <div className="input-select-service input-group">
                  <select
                    value={
                      dateTime && dateTime.service ? dateTime.service : false
                    }
                    className="form-select"
                    onChange={(e) => {
                      setDateTime({ service: e.target.value });
                      setServiceName(e.target.value);
                    }}
                  >
                    <option>Elige un servicio...</option>
                    {store.user_service_hired_id.map((x, index) => {
                      if (x.service_id != 1)
                        return (
                          <option key={index} value={x.name}>
                            {x.name}
                          </option>
                        );
                    })}
                  </select>
                </div>
              </div>
              <div className="datetime-footer">
                <button
                  id="btn-appointment"
                  className="fill me-2 float-end"
                  onClick={() => {
                    actions.setShowDate(true);
                    setShowService(false);
                    setShowCalendar(true);
                    setDateTime({});
                    store.user_service_hired_id.map((x) => {
                      if (x.name == dateTime.service) {
                        setServiceID(x.service_id);
                      }
                    });
                  }}
                >
                  Aceptar
                </button>
              </div>
            </div>
          ) : null}

          {store.showDate == true ? (
            <div>
              <div className="datetime-header py-1">
                <h6 className="pt-2">FECHA</h6>
              </div>
              <div className="datetime-body mt-3">
                <p className="mt-2">
                  Selecciona un día disponible en el calendario
                </p>
              </div>
              <div className="datetime-footer">
                <i
                  className="arrow fa-solid fa-arrow-left-long fa-lg ms-2"
                  type="button"
                  onClick={() => {
                    setShowService(true);
                    actions.setShowDate(false);
                    setShowCalendar(false);
                  }}
                ></i>
              </div>
            </div>
          ) : null}

          {store.showTime == true ? (
            <div>
              <div className="datetime-header py-1">
                <h6 className="pt-2">HORA</h6>
              </div>
              <div className="datetime-body">
                <p className="mt-2">Selecciona una hora disponible</p>
                <div className="hours mx-3 mb-1">
                  {store.dateSelectedTime.map((i, index) => {
                    if (i.is_available == true) {
                      return (
                        <div
                          key={index}
                          className="each-hour"
                          onClick={() => {
                            setHourSelected(i.time);
                            actions.setShowTime(false);
                            setShowAppointment(true);
                            setShowCalendar(false);
                          }}
                        >
                          {i.time}
                        </div>
                      );
                    }
                  })}
                </div>
              </div>
              <div className="datetime-footer">
                <i
                  className="arrow fa-solid fa-arrow-left-long fa-lg ms-2"
                  type="button"
                  onClick={() => {
                    actions.setShowTime(false);
                    actions.setShowDate(true);
                    setShowCalendar(true);
                  }}
                ></i>
              </div>
            </div>
          ) : null}

          {showAppointment == true ? (
            <div>
              <div className="datetime-header py-1">
                <h6 className="pt-2">CITA</h6>
              </div>
              <div className="datetime-body text-start mx-2">
                <p className="datosCita mt-2">Datos de la cita:</p>
                <p>
                  <i>{serviceName + ": "}</i>
                  {(new Date(store.dateSelected).getDay() == 0
                    ? "Domingo, "
                    : new Date(store.dateSelected).getDay() == 1
                    ? "Lunes, "
                    : new Date(store.dateSelected).getDay() == 2
                    ? "Martes, "
                    : new Date(store.dateSelected).getDay() == 3
                    ? "Miércoles, "
                    : new Date(store.dateSelected).getDay() == 4
                    ? "Jueves, "
                    : new Date(store.dateSelected).getDay() == 5
                    ? "Viernes, "
                    : new Date(store.dateSelected).getDay() == 6
                    ? "Sábado, "
                    : null) +
                    store.dateSelected.split("-").reverse().join("/") +
                    " a las " +
                    hourSelected +
                    " horas"}
                </p>
              </div>
              <div className="datetime-footer">
                <i
                  className="arrow fa-solid fa-arrow-left-long fa-lg ms-2"
                  type="button"
                  onClick={() => {
                    actions.setShowTime(true);
                    setShowAppointment(false);
                    setShowCalendar(true);
                  }}
                ></i>

                <button
                  id="btn-appointment"
                  className="fill me-2 float-end"
                  onClick={() => {
                    saveUserAppointment();
                    setShowAppointment(false);
                    setShowCalendar(false);
                    setDataSaved(true);
                    setShowTitle(false);
                  }}
                >
                  Confirmar
                </button>
              </div>
            </div>
          ) : null}
          {dataSaved == true ? (
            <div>
              <div className="datetime-header py-1">
                <h6 className="pt-2">CITA</h6>
              </div>
              <div className="check-msg">
                <i className="fa fa-check-circle text-success ms-5 my-5"></i>
                <div className="d-inline mx-1 text-success">
                  Tu cita se ha guardado correctamente
                </div>
              </div>
              <div>
                <button
                  id="btn-appointment"
                  className="fill btn-appointment float-end me-3"
                  onClick={() => history.push("/user_appointment")}
                >
                  Ver mis citas
                </button>
              </div>
            </div>
          ) : null}
        </div>
      </div>
    </div>
  );
};
