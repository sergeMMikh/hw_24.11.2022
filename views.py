from aiohttp import web


class UserView(web.View):

    def get(self, user_id: int):

        # with Session() as session:
        #     user = get_by_id(user_id, UserModel, session)
        #
        #     if user is None:
        #         raise HttpError(404, 'user not found')
        #
        #     return jsonify({
        #         'user': user.name,
        #         'email': user.email
        #     })

        return web.json_response({
            'class': 'UserView',
            'method': 'get'
        })

    def post(self):
        # json_data = request.json
        # with Session() as session:
        #     try:
        #         new_user = UserModel(**validate(json_data, CreateUserSchema))
        #         session.add(new_user)
        #         session.commit()
        #     except IntegrityError:
        #         raise HttpError(409, 'User name already exists')
        #     return jsonify({'status': 'ok', 'id': new_user.id})
        return web.json_response({
            'class': 'UserView',
            'method': 'post'
        })

    def patch(self, user_id: int):
        # data_to_patch = validate(request.json, PatchUserSchema)
        #
        # with Session() as session:
        #     user = get_by_id(user_id, UserModel, session)
        #
        #     for field, value in data_to_patch.items():
        #         setattr(user, field, value)
        #     session.commit()
        #     return jsonify({'status': 'success', 'id': user.id})
        return web.json_response({
            'class': 'UserView',
            'method': 'patch'
        })

    def delete(self, user_id: int):
        # with Session() as session:
        #     user = get_by_id(user_id, UserModel, session)
        #     session.delete(user)
        #     session.commit()
        #     return jsonify({'status': 'success', 'id': user.id})
        return web.json_response({
            'class': 'UserView',
            'method': 'delete'
        })

    class AdvView(web.View):

        def get(self, adv_id: int):
            # with Session() as session:
            #     adv = get_by_id(adv_id, AdvModel, session)
            #
            #     if adv is None:
            #         raise HttpError(404, 'user not found')
            #
            #     return jsonify({
            #         'Title': adv.title,
            #         'Description': adv.description
            #     })
            return web.json_response({
                'class': 'AdvView',
                'method': 'get'
            })

        def post(self):
            # json_data = request.json
            # with Session() as session:
            #     try:
            #         new_adv = AdvModel(**validate(json_data, CreateAdvSchema))
            #         user_id = get_user_id(json_data, UserModel, session)
            #         setattr(new_adv, 'user_id', user_id)
            #         session.add(new_adv)
            #         session.commit()
            #     except IntegrityError:
            #         raise HttpError(409, 'This title already exists')
            #     return jsonify({'status': 'ok', 'id': new_adv.id})
            return web.json_response({
                'class': 'AdvView',
                'method': 'post'
            })

        def patch(self, adv_id: int):
            # data_to_patch = validate(request.json, PatchAdvSchema)
            # json_data = request.json
            # with Session() as session:
            #     user_id = get_user_id(json_data, UserModel, session)
            #
            #     if user_id != adv_id:
            #         raise HttpError(403, "You don't have rights to delete this advertisement!")
            #
            # adv = get_by_id(adv_id, AdvModel, session)
            #
            # for field, value in data_to_patch.items():
            #     setattr(adv, field, value)
            # session.commit()
            # return jsonify({'status': 'success', 'id': adv.id})
            return web.json_response({
                'class': 'AdvView',
                'method': 'patch'
            })

        def delete(self, adv_id: int):
            #         json_data = request.json
            #         with Session() as session:
            #             user_id = get_user_id(json_data, UserModel, session)
            #
            #             if user_id != adv_id:
            #                 raise HttpError(403, "You don't have rights to delete this advertisement!")
            #
            #             adv = get_by_id(adv_id, AdvModel, session)
            #             session.delete(adv)
            #             session.commit()
            #             return jsonify({'status': 'success', 'id': adv.id, 'user_id': user_id})
            return web.json_response({
                'class': 'AdvView',
                'method': 'delete'
            })
