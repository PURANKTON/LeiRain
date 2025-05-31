from flask import Flask, request, jsonify
from main import HitokotoSystem
from flask_cors import CORS

app = Flask(__name__)
CORS(app)
# 请修改为你的MySQL连接信息
hitokoto = HitokotoSystem(
    host='192.168.10.105',
    user='root',
    password='Xx090202',
    database='layrain'
)


@app.route('/api/hitokoto', methods=['GET'])
def get_hitokoto():
    """获取随机一言"""
    category = request.args.get('category')
    hitokoto_data = hitokoto.get_random_hitokoto(category)

    if hitokoto_data:
        return jsonify({
            'code': 200,
            'message': '获取成功',
            'data': hitokoto_data
        })
    else:
        return jsonify({
            'code': 404,
            'message': '没有找到一言'
        }), 404


@app.route('/api/hitokoto/<int:hitokoto_id>', methods=['GET'])
def get_hitokoto_by_id(hitokoto_id):
    """根据ID获取一言"""
    hitokoto_data = hitokoto.get_hitokoto_by_id(hitokoto_id)

    if hitokoto_data:
        return jsonify({
            'code': 200,
            'message': '获取成功',
            'data': hitokoto_data
        })
    else:
        return jsonify({
            'code': 404,
            'message': '没有找到该一言'
        }), 404


@app.route('/api/hitokoto', methods=['POST'])
def add_hitokoto():
    """添加一言"""
    data = request.json
    required_fields = ['content']

    for field in required_fields:
        if field not in data:
            return jsonify({
                'code': 400,
                'message': f'缺少必要字段: {field}'
            }), 400

    hitokoto_id = hitokoto.add_hitokoto(
        content=data['content'],
        author=data.get('author'),
        source=data.get('source'),
        category=data.get('category')
    )

    if hitokoto_id:
        return jsonify({
            'code': 201,
            'message': '添加成功',
            'data': {'id': hitokoto_id}
        }), 201
    else:
        return jsonify({
            'code': 500,
            'message': '添加失败'
        }), 500


@app.route('/api/hitokoto/<int:hitokoto_id>', methods=['PUT'])
def update_hitokoto(hitokoto_id):
    """更新一言"""
    data = request.json

    if not data:
        return jsonify({
            'code': 400,
            'message': '没有提供更新数据'
        }), 400

    success = hitokoto.update_hitokoto(
        hitokoto_id,
        content=data.get('content'),
        author=data.get('author'),
        source=data.get('source'),
        category=data.get('category')
    )

    if success:
        return jsonify({
            'code': 200,
            'message': '更新成功'
        })
    else:
        return jsonify({
            'code': 404,
            'message': '没有找到该一言或更新失败'
        }), 404


@app.route('/api/hitokoto/<int:hitokoto_id>', methods=['DELETE'])
def delete_hitokoto(hitokoto_id):
    """删除一言"""
    success = hitokoto.delete_hitokoto(hitokoto_id)

    if success:
        return jsonify({
            'code': 200,
            'message': '删除成功'
        })
    else:
        return jsonify({
            'code': 404,
            'message': '没有找到该一言'
        }), 404


@app.route('/api/hitokoto/list', methods=['GET'])
def list_hitokoto():
    """获取一言列表"""
    limit = int(request.args.get('limit', 10))
    offset = int(request.args.get('offset', 0))
    category = request.args.get('category')

    hitokoto_list = hitokoto.list_hitokoto(limit, offset, category)
    total = hitokoto.count_hitokoto(category)

    return jsonify({
        'code': 200,
        'message': '获取成功',
        'data': {
            'list': hitokoto_list,
            'total': total,
            'limit': limit,
            'offset': offset
        }
    })


@app.route('/api/categories', methods=['GET'])
def get_categories():
    """获取分类列表"""
    categories = hitokoto.get_categories()

    return jsonify({
        'code': 200,
        'message': '获取成功',
        'data': categories
    })


if __name__ == '__main__':
    app.run(host="0.0.0.0",debug=True,port=5000)