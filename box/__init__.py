"""
+---------------------------------------------------------------------------------+
|														    ****************      |                                   
|										                     *              *     |                                   
|										                       *             *    |                                    
|	______ _                          ______                    *             *   |                                  
|	|  _  (_)                         | ___ \                    **************   |                                   
|	| | | |_  __ _ _ __   __ _  ___   | |_/ / _____  __       ***             *   |                                   
|	| | | | |/ _` | '_ \ / _` |/ _ \  | ___ \/ _ \ \/ /		***************** *   |                                   
|	| |/ /| | (_| | | | | (_| | (_) | | |_/ / (_) >  <      *       *       * *   |                                   
|	|___/ | |\__,_|_| |_|\__, |\___/  \____/ \___/_/\_\     *       *       * *   |                                    
|	     _/ |             __/ |                             *    **** ***   * *   |                                   
|	    |__/             |___/                              *    ** *  **   * *   |                                    
|															*    ****  **   * *   |                                   
|															*          **   * *   |                                    
|	a simple django template fragment mechanism				*       ****    **    |                                    
|															*****************     |
+---------------------------------------------------------------------------------+	

"""
from django.template.defaulttags import register
from django.template import loader
from django.template.context import BaseContext


__name__ = 'Django Box'
__version__= '0.0.4.dev1'

def main():
  return "main"

@register.inclusion_tag('templates/default.html' , takes_context=True)
def box(context, box_name,  *args, **kwargs):
    try:
        module_path = kwargs['path']

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


class BoxView(object):
    template_name = 'boxes/base.html'
    context = {}

    def __init__(self, *args, **kwargs):
        self.template = loader.get_template(self.template_name)

    def result(self):
        return self.template.render(BaseContext(self.context))

    def get_context(self):
        if 'include_context' in self.context and self.context['include_context']:
            return self.context['parent_context']

    def get_argument(self, key):
        if key in self.context['args']:
            return self.context['args'][key]
        else:
            return False
