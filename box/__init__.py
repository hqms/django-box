def main():
  return "main"

def box(context, box_name, module_path, *args, **kwargs):
    try:

        mod = __import__(module_path + box_name, fromlist=['*'])
        obj = getattr(mod, box_name)

        if 'include_context' in kwargs and kwargs['include_context'] == True:
            obj.context['parent_context'] = context
            obj.context['include_context'] = True
        else:
            kwargs['include_context'] = False

        obj.context['args'] = kwargs

        return {'obj': obj}
    except ImportError:
        print 'Box "{0}" not found '.format(box_name)
    except AttributeError:
        print 'Class "{0}" not found or mistype'.format(box_name)
    except Exception as e:
        print 'Error: "{0}" on "{1}"'.format(e.message, box_name)
