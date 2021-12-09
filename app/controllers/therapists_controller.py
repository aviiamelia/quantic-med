from flask import request, jsonify, current_app
from psycopg2.errorcodes import UNIQUE_VIOLATION
import sqlalchemy
import psycopg2
from sqlalchemy.exc import IntegrityError
from app.exc.excessoes import NumericError, PasswordMinLengthError, WrongKeyError
from app.models.therapists_model import Therapists
from app.controllers.verifications import is_numeric_data, verify_keys, password_min_length
from app.models.specialties_model import Specialties


def create_therapist():
    session = current_app.db.session

    try:
        data = request.get_json()
        verify_keys(data, "therapist", "patch")

        specialties_data = data.pop('ds_specialties')

        inserted_data = Therapists(**data)

        """[comment]
            The code below lists and serializes the categories that a therapist has.
            Add a new category if it doesn't exist
        """
        for specialty in specialties_data:
            filtered_data = Specialties.query.filter_by(
                nm_specialty=specialty['nm_specialty']).first()
            if not filtered_data:
                new_specialty = Specialties(**specialty)
                inserted_data.specialties.append(new_specialty)
            else:
                inserted_data.specialties.append(filtered_data)

        session.add(inserted_data)
        session.commit()

        return jsonify(inserted_data), 201

    except WrongKeyError as error:
        return jsonify({"Error": error.value}), 400
    except NumericError as error:
        return jsonify(error.value), 400
    except PasswordMinLengthError as error:
        return jsonify(error.value), 400
    except IntegrityError as e:
        if e.orig.pgcode == UNIQUE_VIOLATION:
            return {"error": "Cpf, crm ou username já cadastrados"}, 409
        return str(e), 404


def update_therapist(id):
    session = current_app.db.session

    data = request.get_json()

    try:
        verify_keys(data, "therapist", "patch")

        filtered_data = Therapists.query.get(id)
        if filtered_data is None:
            return {"error": "Terapeuta não encontrado"}

        for key, value in data.items():
            setattr(filtered_data, key, value)

        session.add(filtered_data)
        session.commit()
    except IntegrityError as e:
        if e.orig.pgcode == UNIQUE_VIOLATION:
            return {"error": "Cpf, crm ou username já cadastrados"}, 409

    return jsonify(filtered_data), 200


def delete_therapist(id):
    session = current_app.db.session

    filtered_data = Therapists.query.get(id)
    if filtered_data is None:
        return {"error": "Terapeuta não encontrado"}

    session.delete(filtered_data)
    session.commit()

    return '', 204


def get_all_therapists():

    page = request.args.get('page', 1)
    per_page = request.args.get('per_page', 5)
    order = request.args.get('order_by', 'id_therapist')
    direction = request.args.get('dir', False)

    filtered_data = Therapists.query.order_by(getattr(Therapists, order)).paginate(
        int(page), int(per_page), error_out=False).items

    """[comment]
        The following code lists the Therapists object's to allow the function reverse
    """
    response = list()
    for item in filtered_data:
        therapist_data = dict(item)
        response.append(therapist_data)

    if direction:
        response.reverse()

    return jsonify(response), 200


def get_therapist_by_id(id):
    filtered_data = Therapists.query.get(id)
    if filtered_data is None:
        return {"erro": "Recepcionista não encontrado"}

    return jsonify(filtered_data), 200
